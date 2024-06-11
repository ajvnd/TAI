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
        toolbar: {
            visible: true,
            items: ["addRowButton", {
                name: "x",
                location: "before",
                widget: "dxSelectBox",
                options: {
                    width: "30vw",
                    dataSource: new DevExpress.data.CustomStore({
                        key: "id",
                        load: function () {
                            return $.getJSON(Project_URL);
                        },
                        insert: function (values) {
                            return $.ajax({
                                url: Project_URL,
                                method: "POST",
                                contentType: "application/json",
                                data: JSON.stringify(values)
                            });
                        },
                    }),
                }
            },]
        },
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
                formItem: {
                    visible: false
                },
                alignment: "center",
                width: "10vh"
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
                    },
                    columns: [
                        {
                            name: "id",
                            dataField: "id",
                            formItem: {
                                visible: false
                            },
                            alignment: "center",
                            width: "12vh"
                        },
                        {
                            name: "title",
                            dataField: "title",
                            dataType: "string",
                            alignment: "center",
                        },
                        {
                            name: "start_date",
                            dataField: 'start_date',
                            dataType: 'date',
                            alignment: "center"
                        },
                        {
                            name: "due_date",
                            dataField: 'due_date',
                            dataType: 'date',
                            calculateDisplayValue(f) {
                                const givenDate = new Date(f.due_date).getTime();  // Convert given date to timestamp
                                const now = Date.now();  // Get current timestamp

                                if (givenDate < now) {
                                    return "The time is finished";
                                } else {
                                    const timeDifference = givenDate - now;
                                    const daysRemaining = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));
                                    return `${daysRemaining} days remaining`;
                                }
                            },
                            alignment: "center"
                        },
                        {
                            name: "is_completed",
                            dataField: "is_completed",
                            caption: 'Completed',
                            dataType: 'boolean',
                            alignment: "center",
                            width: "16vh",
                        }]

                }).appendTo(container);
            }
        }
    });

})