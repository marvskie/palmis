ej.base.enableRipple(true);

    
var dataManger = new ej.data.DataManager({
    url: '/api/v1/task1/data',
    crudUrl: '/api/v1/task1/crud',
    adaptor: new ej.data.UrlAdaptor(),
    crossDomain: true,
    headers: [{"Authorization" : window.u}]
});

var scheduleObj = new ej.schedule.Schedule({
    height: '80%',
    width: '80%',
    selectedDate: Date.now(),
    eventSettings: { dataSource: dataManger },
    dragStart: function (args) {
        args.navigation.enable = true;
    }, 
    dataBinding: function(ev){
        let tasks = ev.result.tasks
        let scheduleData = []
        tasks.forEach(task => {
          let custom = {
                      Id: task.custom_id,
                      Subject: task.title,
                      Description: task.description,
                      StartTime: new Date(task.start_time),
                      EndTime: new Date(task.end_time),
                      IsAllDay: false, 
                      Location: task.location, 
                      UserId: window.u
                  }
          scheduleData.push(custom)
        });
        ev.result = scheduleData
        console.log('data....')
        console.log(scheduleData)
        console.log(ev.result)
      }
});
scheduleObj.appendTo('#Schedule');
var currentDate = new ej.calendars.DatePicker({
    value: new Date(),
    showClearButton: false,
    change: function (args) {
        scheduleObj.selectedDate = args.value;
        scheduleObj.dataBind();
    }
});
currentDate.appendTo('#scheduledate');


$("#refreshCalendar").click(function () {
    window.location.reload(true);
  });