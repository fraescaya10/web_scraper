from . import ma


class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'role', 'company', 'city',
                  'division', 'department', 'type')
