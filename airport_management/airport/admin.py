from django.contrib import admin
from airport.models import *

admin.site.register(User)
admin.site.register(Flight)
admin.site.register(Airport)
admin.site.register(Aeroplane)
admin.site.register(Role)
admin.site.register(UserRoleMapping)
admin.site.register(Runway)
admin.site.register(NoticeBoard)
admin.site.register(TicketCounter)
admin.site.register(LuggageCounter)


