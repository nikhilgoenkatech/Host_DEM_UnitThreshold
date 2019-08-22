#all the constants
API_CALL = 'entity/infrastructure/hosts'
TIMESERIES_API="timeseries/com.dynatrace.builtin:host.availability?includeData=true&&relativeTime=10mins"
APP_BILLING_API = "metrics/series/builtin%3Abilling.apps.web.sessionsByApplication%3Afold(value)?pageSize=0&resolution=120&from=now-3y"
SYNC_BILLING_API = "metrics/series/builtin%3Abilling.synthetic.actions%3Afold(value)?pageSize=0&resolution=120&from=now-3y"
HTTP_BILLING_API = "metrics/series/builtin%3Abilling.synthetic.requests%3Afold(value)?pageSize=0&resolution=120&from=now-3y"
