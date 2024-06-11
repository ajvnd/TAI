$(function () {

    const Project_URL = "http://127.0.0.1:8000/projects";
    const Task_URL = "http://127.0.0.1:8000/tasks";
    const Sub_Task_URL = "http://127.0.0.1:8000/sub_tasks";

    $("#tasksGrid").dxDataGrid({
        dataSource: new DevExpress.data.CustomStore({
            key: "id",
            load: function () {
                return $.getJSON(Task_URL);
            },
            insert: function (values) {
                return $.ajax({
                    url: Task_URL,
                    method: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(values)
                });
            },
            update: (key, values) => {
                return $.ajax({
                    url: `${Task_URL}/${encodeURIComponent(key)}`,
                    method: "PUT",
                    contentType: "application/json",
                    data: JSON.stringify(values)
                });
            },
            remove: (key) => {
                return $.ajax({
                    url: `${Task_URL}/${encodeURIComponent(key)}`,
                    method: "DELETE",
                });
            },
        }),
        height: "100vh",
        width: "100vw",
        showColumnLines: true,
        paging: {
            enabled: true,
            pageSize: 10,
        },
        pager: {
            visible: true,
            displayMode: "full",
            allowedPageSizes: [10, 20, 50, 100],
            showPageSizeSelector: true,
            showNavigationButtons: true,
            showInfo: true,
        },

        editing: {
            mode: 'row',
            allowAdding: true,
            allowUpdating: true,
            allowDeleting: true,
        },
        columns: [
            {
                name: "id",
                dataField: "id",
                visible: false,
                formItem: {
                    visible: false
                },
                alignment: "center",
            },
            {
                name: "title",
                dataField: "title",
                dataType: "string",
                alignment: "center",
            },
            {
                name: "is_completed",
                dataField: "is_completed",
                caption: "Completed",
                dataType: "boolean",
                alignment: "center",
                width: "14vh",
            },
            {
                name: "buttons",
                type: "buttons",
                buttons: [
                    {
                        name: "generate",
                        icon: "datapie",
                        onClick() {
                            alert("Generate Tasks");
                        }
                    }, "edit", "delete",]
            }
        ],


        masterDetail: {
            enabled: true,

            template(container, options) {
                $('<div>').dxDataGrid({
                    width: "100vw",
                    showColumnLines: true,
                    dataSource: new DevExpress.data.CustomStore({
                        key: "id",
                        load: function () {
                            return $.getJSON(`${Task_URL}/${encodeURIComponent(options.data.id)}/sub_tasks`);
                        },
                        insert: function (values) {
                            return $.ajax({
                                url: Task_URL,
                                method: "POST",
                                contentType: "application/json",
                                data: JSON.stringify(values)
                            });
                        },
                        update: (key, values) => {
                            return $.ajax({
                                url: `${Sub_Task_URL}/${encodeURIComponent(key)}`,
                                method: "PUT",
                                contentType: "application/json",
                                data: JSON.stringify(values)
                            });
                        },
                        remove: (key) => {
                            return $.ajax({
                                url: `${Sub_Task_URL}/${encodeURIComponent(key)}`,
                                method: "DELETE",
                            });
                        },
                    }),
                    editing: {
                        mode: 'form',
                        allowAdding: true,
                        allowUpdating: true,
                        allowDeleting: true,
                        form: {
                            labelLocation: "left"
                        }
                    },
                    columns: [
                        {
                            name: "id",
                            dataField: "id",
                            visible: false,
                            formItem: {
                                visible: false
                            },
                            alignment: "center",
                        },
                        {
                            name: "title",
                            dataField: "title",
                            dataType: "string",
                            alignment: "center",
                        },
                        {
                            name: "duration",
                            dataField: "duration",
                            dataType: "number",
                            alignment: "center",
                            visible: false,
                        },
                        {
                            name: "spend",
                            dataField: "spend",
                            dataType: "number",
                            alignment: "center",
                            visible: false,
                        },
                        {
                            name: "progress",
                            formItem: {
                                visible: false
                            },
                            cellTemplate(element, colData) {
                                element.append($("<div>").dxProgressBar({
                                    min: 0,
                                    max: 100,
                                    value: (colData.data.spend / colData.data.duration) * 100,
                                }))
                            }
                        },
                        {
                            name: "is_completed",
                            dataField: "is_completed",
                            caption: '',
                            dataType: 'boolean',
                            alignment: "center",
                            width: "5vh",
                        },
                        {
                            name: "buttons",
                            type: "buttons",
                            buttons: [
                                {
                                    name: "generate",
                                    icon: "spinnext",
                                    onClick(e) {
                                        if (e.row.data.spend === e.row.data.duration) {
                                            DevExpress.ui.dialog.alert("the task is finished")
                                        } else {
                                            DevExpress.ui.dialog.alert("starting...")
                                        }

                                    }
                                }, "edit", "delete",]
                        }
                    ]

                }).appendTo(container);
            }
        }
    });

})