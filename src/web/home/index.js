$(function () {

    const Project_URL = "http://127.0.0.1:8000/projects";
    const Task_URL = "http://127.0.0.1:8000/tasks";
    const Sub_Task_URL = "http://127.0.0.1:8000/sub_tasks";

    let manage_popup = $("#manage_popup").dxPopup({}).dxPopup('instance');

    let toolbar = $("#toolbar").dxToolbar({
        height: "2vh",
        width: "100vw",
        items: [
            {
                widget: "dxSelectBox",
                options: {
                    onSelectionChanged(e) {
                        localStorage.setItem("selected_project_id", e.selectedItem.id)
                        task_grid.refresh()
                    },
                    width: "20vw",
                    valueExpr: "id",
                    displayExpr: "title",

                    dataSource: new DevExpress.data.CustomStore({
                        key: "id",
                        load: function () {
                            return $.getJSON(Project_URL);
                        },
                    }),
                }
            },
            {
                widget: "dxMenu",
                location: 'before',
                options: {
                    items: [
                        {
                            text: "Manage",
                            items: [
                                {
                                    text: 'projects',
                                    onClick() {
                                        manage_popup.show()
                                    }
                                }
                            ]

                        },
                    ]
                }
            },
            {
                widget: "dxButton",
                location: "after",
                options: {
                    icon: "sun",
                    onClick: function (e) {
                        if (e.component.option("icon") === "sun")
                            e.component.option("icon", "moon")
                        else
                            e.component.option("icon", "sun")
                    }
                }
            }
        ]
    }).dxToolbar('instance')

    let task_grid = $("#tasksGrid").dxDataGrid({
        dataSource: new DevExpress.data.CustomStore({
            key: "id",
            load: function () {
                return $.getJSON(`${Task_URL}/${encodeURIComponent(localStorage.getItem("selected_project_id") ?? 1)}`);
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
        height: "98vh",
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
        ],

        //TODO: Hide duration, start date, end date
        masterDetail: {
            enabled: true,
            template(container, options) {
                let db = $('<div>').dxDataGrid({
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
                            name: "start_date",
                            dataField: "start_date",
                            dataType: "date",
                            alignment: "center",
                            width: "10vh",
                            formItem: {
                                visible: false
                            }
                        },
                        {
                            name: "pomodoros",
                            dataField: "pomodoros",
                            dataType: "pomodoros",
                            alignment: "center",
                            width: "10vh",
                            calculateDisplayValue: (e) => {
                                return (e.progress / 25).toFixed(1) + " of " + e.pomodoros;
                            }
                        },
                        {
                            name: "progress",
                            dataField: "progress",
                            dataType: "number",
                            alignment: "center",
                            cellTemplate(element, colData) {
                                element.append($("<div>").dxProgressBar({
                                    min: 0,
                                    max: 100,
                                    value: (colData.data.progress / colData.data.duration) * 100,
                                }))
                            },
                        },
                        {
                            name: "duration",
                            dataField: "duration",
                            dataType: "number",
                            alignment: "center",
                            visible: false,
                        },
                        {
                            name: "end_date",
                            dataField: "end_date",
                            dataType: "date",
                            alignment: "center",
                            width: "10vh",
                            formItem: {
                                visible: false
                            }
                        },
                        {
                            name: "is_completed",
                            dataField: "is_completed",
                            dataType: 'boolean',
                            alignment: "center",
                            width: "10vh",
                        },
                        //TODO: disable the button that has completed pomodoro
                        {
                            name: "buttons",
                            dataField: "buttons",
                            type: "buttons",
                            buttons: [{
                                icon: "arrowright",
                                onClick(e, d) {
                                    //TODO: list of interval, push, pop, pause, play, stop
                                    let progress = e.row.data.progress;
                                    const interval = setInterval(() => {

                                            progress += 1;

                                            if (progress === e.row.data.duration)
                                                clearInterval(interval);

                                            return $.ajax({
                                                url: `${Sub_Task_URL}/${encodeURIComponent(e.row.data.id)}/progression`,
                                                method: "PUT",
                                                contentType: "application/json",
                                                data: JSON.stringify({progress: progress}),
                                                success: (response) => {
                                                    sub_task_grid.cellValue(e.row.rowIndex, "progress", progress + 1);
                                                    sub_task_grid.refresh(true);
                                                    setTimeout(() => {
                                                        $(sub_task_grid.getCellElement(e.row.rowIndex, "progress")).css('background-color', 'white');
                                                    }, 3000)

                                                }
                                            });

                                        },
                                        1000
                                    )

                                }
                            }, "edit", "delete"]
                        }

                    ]

                });

                db.appendTo(container);
                let sub_task_grid = db.dxDataGrid('instance')
            }
        }
    }).dxDataGrid('instance');

})