import colander
import deform.widget

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .models import DBSession, Record


class MyPage(colander.MappingSchema):
    email = colander.SchemaNode(colander.String())
    name = colander.SchemaNode(colander.String())


class MyViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def my_form(self):
        schema = MyPage()
        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.my_form.get_widget_resources()

    @view_config(route_name='my_view', renderer='templates/home_view.pt')
    def my_view(self):
        records = DBSession.query(Record).order_by(Record.email)
        return dict(email='My View', records=records)

    @view_config(route_name='mypage_add', renderer='templates/mypage_addedit.pt')
    def mypage_add(self):
        form = self.my_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.my_form.validate(controls)
            except deform.ValidationFailure as e:
                # Form is NOT valid
                return dict(form=e.render())

            # Add a new page to the database
            new_email = appstruct['email']
            new_name = appstruct['name']
            DBSession.add(Record(name=new_name, email=new_email))

            # Get the new ID and redirect
            record = DBSession.query(Record).filter_by(email=new_email).one()
            new_id = record.id

            url = self.request.route_url('mypage_view', id=new_id)
            return HTTPFound(url)

        return dict(form=form)


    @view_config(route_name='mypage_view', renderer='templates/mypage_view.pt')
    def mypage_view(self):
        # id = int(self.request.matchdict['id'])
        # record = DBSession.query(Record).filter_by(id=id).one()
        # return dict(record=record)
        records = DBSession.query(Record).order_by(Record.id)
        return dict(email='My View', records=records)


    @view_config(route_name='delete_record', permission='edit')
    def delete_record(self):
        id = int(self.request.matchdict['id'])
        value = DBSession.query(Record).filter_by(id=id).one()
        DBSession.delete(value)

        url = self.request.route_url('mypage_view')
        return HTTPFound(url)

    @view_config(route_name='delete_record_ajax', permission='edit')
    def delete_record_ajax(self):
        print(self.request.params)
        id = int(self.request.matchdict['id'])
        print("idd:  "+ str(id))
        value = DBSession.query(Record).filter_by(id=id).one()
        DBSession.delete(value)
        records = DBSession.query(Record).order_by(Record.id)
        return {'records' : records}
