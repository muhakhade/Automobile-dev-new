from django.conf.urls import url
from automobile import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # root and auth
    url(r'^$', views.RootView.as_view()),
    
    # BUAT APPS 
    url(r'^api/user/register/$', views.register),
    url(r'^api/user/auth/$', views.auth),
    url(r'^api/cars/all/$', views.showAllCar),
    url(r'^api/cars/user-select/$', views.selectCar),
    url(r'^api/user/get-breaking-data/$', views.getBreakingSystemByEmail),
    url(r'^api/user/get-breaking-data/summary-recommendation/$', views.getIntervalCheckBreakingSystem),
    url(r'^api/user/get-temperature-rise-data/$', views.getTemperatureRiseByEmail),
    url(r'^api/user/get-air-filter-data/$', views.getAirFilterByEmail),
    url(r'^api/user/get-air-filter-data/by-month/$', views.getAirFilterByEmailGroupByMonth),
    url(r'^api/user/get-air-filter-data/estimated/$', views.getEstimatedLifetimeAirFilter),    
    url(r'^api/user/get-fuel-system-data/$', views.getFuelSystemByEmail),
    
    

    # BUAT RASPI 
    url(r'^api/raspi/insert/breaking/$', views.insertBreakingSystem),
    url(r'^api/raspi/insert/breaking/special-case/$', views.insertBreakingSystemSpecialCase), 
    url(r'^api/raspi/insert/temperature-rise/$', views.insertTemperatureRise),
    url(r'^api/raspi/insert/temperature-rise/special-case/$', views.insertTemperatureRiseSpecialCase),
    url(r'^api/raspi/insert/air-filter/$', views.insertAirFilter),
    url(r'^api/raspi/insert/fuel-system/$', views.insertFuelSystem),
    url(r'^api/raspi/insert/oil-lifetime/$', views.insertOilLifetime),
    url(r'^api/raspi/insert/emission-system/$', views.insertEmissionSystem),
    url(r'^api/raspi/insert/fuel-consumption/$', views.insertFuelConsumption),

    # MISC
    url(r'^api/cars/add/$', views.insertCar),
    url(r'^api/seed/breaking-system/$', views.seedBreakingData),
    url(r'^api/seed/temperature-rise/$', views.seedTemperatureData),
    url(r'^api/seed/air-filter/$', views.seedAirFilter),
    url(r'^api/seed/fuel-system/$', views.seedFuelData),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
