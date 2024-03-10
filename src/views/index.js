$(function () 
{
    const SERVICE_URL = "http://127.0.0.1:8000/tasks";

    $("#tasksGrid").dxDataGrid({
        dataSource: new DevExpress.data.CustomStore({
            key: "_id",
            load: function () {
                return $.getJSON(SERVICE_URL);
            },
            insert:function(values){
                return $.ajax({
                    url: SERVICE_URL,
                    method: "POST",
                    data: JSON.parse(values)
                    });
            },
            update: (key, values) => {
                return $.ajax({
                    url: SERVICE_URL + "/" + encodeURIComponent(key),
                    method: "PUT",
                    contentType: "application/json",
                    data: JSON.parse({
                        task:{
                        _id:key,
                        title:values.title
                        }
                    })
                });
            },
            remove: (key) => {
                return $.ajax({
                    url: SERVICE_URL + "/" + encodeURIComponent(key),
                    method: "DELETE",
                });
            },
        }),
        paging: {
            enabled: false,
          },
        editing: {
            mode: 'form',
            allowUpdating: true,
            allowAdding: true,
            allowDeleting: true,
          },
        columns: [
            "_id",
            "title",
        ]
    });
})