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
                $('<div>').dxDataGrid({
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
                            name: "progress",
                            dataField: "progress",
                            dataType: "number",
                            alignment: "center",
                            formItem: {
                                visible: false
                            },
                            calculateDisplayValue: (e) => {
                                return `${parseInt(e.progress / Default_Pomodoro_time * 100)}%`
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
                            type: "buttons",
                            buttons: [{
                                icon: "arrowright",
                                disabled: (e) => {
                                    return e.row.data.is_completed;
                                },
                                onClick(e, d) {

                                    let timer = get_timer(() => {
                                        $.ajax({
                                            url: `${Sub_Task_URL}/${encodeURIComponent(e.row.data.id)}/progression`,
                                            method: "PUT",
                                            contentType: "application/json",
                                            data: JSON.stringify({progress: Default_Pomodoro_time}),
                                            success: (response) => {
                                                e.component.refresh()
                                            }
                                        });
                                        timer.hide()
                                    })
                                    timer.show()
                                }
                            }, "edit", "delete"]
                        }

                    ]

                }).appendTo(container)
            }
        }
    }).dxDataGrid('instance');

})

