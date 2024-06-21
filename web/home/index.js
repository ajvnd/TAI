$(function () {

    const Project_URL = "http://127.0.0.1:8000/projects";
    const Task_URL = "http://127.0.0.1:8000/tasks";
    const Sub_Task_URL = "http://127.0.0.1:8000/sub_tasks";

    const Default_Project_Id = 1;

    function getProjectId() {
        return localStorage.getItem("selected_project_id") ?? Default_Project_Id;
    }

    $("#toolbar").dxToolbar({
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
                    width: "30vw",
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
        ]
    });

    let task_grid = $("#tasksGrid").dxDataGrid({
        dataSource: new DevExpress.data.CustomStore({
            key: "id",
            load: function () {
                return $.getJSON(`${Task_URL}/${encodeURIComponent(getProjectId())}`);
            },
            insert: function (values) {
                values.project_id = getProjectId()
                return $.ajax({
                    url: Task_URL,
                    method: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(values)
                });
            },
            update: (key, values) => {
                values.project_id = getProjectId()
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

        editing: {
            mode: 'row',
            allowAdding: true,
            allowUpdating: true,
            allowDeleting: true,
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
        sorting: {
            mode: "none"
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
        masterDetail: {
            enabled: true,
            template(container, options) {
                let db = $('<div>').dxDataGrid({
                    width: "100vw",
                    showColumnLines: true,
                    columnHidingEnabled: true,
                    dataSource: new DevExpress.data.CustomStore({
                        key: "id",
                        load: function () {
                            return $.getJSON(`${Task_URL}/${encodeURIComponent(options.data.id)}/sub_tasks`);
                        },
                        insert: function (values) {
                            values.task_id = options.data.id;
                            return $.ajax({
                                url: Sub_Task_URL,
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
                    sorting: {
                        mode: "none"
                    },
                    columns: [
                        {
                            name: "id",
                            dataField: "id",
                            visible: false,
                            alignment: "center",
                            formItem: {
                                visible: false
                            },
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
                            hidingPriority: 0,
                            formItem: {
                                visible: false
                            }
                        },
                        {
                            name: "pomodoros",
                            dataField: "pomodoros",
                            dataType: "pomodoros",
                            alignment: "center",
                            hidingPriority: 2,
                            calculateDisplayValue: (e) => {
                                return (e.progress / 25).toFixed(1) + " of " + e.pomodoros;
                            }
                        },
                        {
                            name: "progress",
                            dataField: "progress",
                            dataType: "number",
                            alignment: "center",
                            hidingPriority: 3,
                            formItem: {
                                visible: false
                            },
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
                            formItem: {
                                visible: false
                            }
                        },
                        {
                            name: "end_date",
                            dataField: "end_date",
                            dataType: "date",
                            alignment: "center",
                            hidingPriority: 1,
                            formItem: {
                                visible: false
                            }
                        },
                        {
                            name: "is_completed",
                            dataField: "is_completed",
                            dataType: 'boolean',
                            alignment: "center",
                        },
                        {
                            name: "buttons",
                            dataField: "buttons",
                            type: "buttons",
                            buttons: [{
                                icon: "arrowright",
                                disabled: (e) => {
                                    return e.row.data.is_completed;
                                },
                                onClick(e, d) {
                                    //TODO: Increasing
                                    let interval = get_interval(e.row.data.id)

                                    if (interval === null) {

                                        interval = {};
                                        interval.is_running = true;
                                        interval.progress = e.row.data.progress + 1
                                        interval.operation = () => {
                                            $.ajax({
                                                url: `${Sub_Task_URL}/${encodeURIComponent(e.row.data.id)}/progression`,
                                                method: "PUT",
                                                contentType: "application/json",
                                                data: JSON.stringify({progress: interval.progress}),
                                                success: (response) => {
                                                    sub_task_grid.cellValue(e.row.rowIndex, "progress", interval.progress);
                                                    sub_task_grid.refresh(true);
                                                    setTimeout(() => {
                                                        $(sub_task_grid.getCellElement(e.row.rowIndex, "progress")).css('background-color', 'white');
                                                    }, 3000)

                                                }
                                            });
                                        }
                                        set_interval(e.row.data.id, interval)
                                        continue_interval(e.row.data.id)
                                    } else {
                                        if (interval.is_running) {
                                            halt_interval(e.row.data.id)
                                        } else {
                                            continue_interval(e.row.data.id)
                                        }
                                    }
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


let intervals = [];

function get_interval(task_id) {
    if (intervals[task_id] != null)
        return intervals[task_id]
    return null
}

function set_interval(task_id, interval) {
    intervals[task_id] = interval;
}

function halt_interval(task_id) {
    intervals[task_id].is_running = false;
    clearInterval(intervals[task_id].interval);
}

function continue_interval(task_id) {
    intervals[task_id].is_running = true;
    intervals[task_id].interval = setInterval(() => {
        intervals[task_id].operation()
    }, 6000);
}

