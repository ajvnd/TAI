function get_profile_pop_up() {
    return $("#profile_pop_up").dxPopup({}).dxPopup('instance');
}

function get_settings_pop_up() {
    return $("#settings_pop_up").dxPopup({}).dxPopup('instance');
}

$(function () {

    const Project_URL = "http://127.0.0.1:8000/projects";
    const Task_URL = "http://127.0.0.1:8000/tasks";

    $("#toolbar").dxToolbar({
        elementAttr: {
            class: "dx-theme-border-color-as-background-color",
        },
        items: [
            {
                widget: 'dxButton',
                location: "before",
                options: {
                    icon: 'menu',
                    onClick() {
                        drawer.toggle()
                    }
                }
            },
            {
                widget: 'dxSelectBox',
                locateInMenu: "auto",
                options: {
                    icon: 'search',
                    width: "100%",
                }
            },
            {
                widget: 'dxDropDownButton',
                location: "after",
                locateInMenu: "auto",
                options: {
                    text: "ahmadjavadi17@gmail.com",
                    icon: 'user',
                    splitButton: true,
                    items: [
                        {
                            icon: "accountbox",
                            text: "Profile",
                            onClick() {
                                let profile_pop_up = get_profile_pop_up();
                                profile_pop_up.show()
                            }
                        },
                        {
                            icon: "preferences",
                            text: "Settings",
                            onClick() {
                                let settings_pop_up = get_settings_pop_up();
                                settings_pop_up.show()
                            }
                        },
                        {
                            icon: "arrowleft",
                            text: "Sign Out"
                        }]
                }
            }
        ]
    });

    $("#summary").dxForm({
        colCount: 2,
        readOnly: true,
        items: [{
            widget: 'dxTextBox',
            dataField: "tasks_to_complete",
            label: {
                text: "Tasks to complete",
                alignment: "center"
            },
            editorOptions: {
                stylingMode: "underlined",
            }
        }, {
            widget: 'dxTextBox',
            dataField: "completed_tasks",
            label: {
                text: "Completed tasks",
                alignment: "center"
            },
            editorOptions: {
                stylingMode: "underlined",
            }
        }]
    })

    const drawer = $("#drawer").dxDrawer({

        template() {

            return $("<div/>").dxList({
                elementAttr: {
                    class: "dx-theme-border-color-as-background-color",
                    id: "drawer-content"
                },
                width: "200px",
                grouped: true,
                collapsibleGroups: true,
                items: [
                    {
                        key: "Due Date",
                        items: [
                            {
                                text: "Today",
                                badge: "27",
                            },
                            {
                                text: "Tomorrow",
                                badge: "13"
                            },
                            {
                                text: "This Week",
                                badge: "43"
                            },
                            {
                                text: "Some Days", badge: "61",
                            }
                        ]
                    },
                    {
                        key: "Projects",
                        items: [
                            {
                                text: "Project 1",
                                badge: "50",
                            }, {
                                text: "Project 2",
                                badge: "43",
                            },
                            {
                                text: "Project 3",
                                badge: "21",
                            },
                            {
                                icon: "more",
                                text: "More"
                            }
                        ]
                    }]
            })
        }

    }).dxDrawer('instance');


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
            allowedPageSizes: [10, 20, 50, 100],
            showPageSizeSelector: true,
            showNavigationButtons: true,
            displayMode: "adaptive",
            showInfo: true,
        },
        sorting: {
            mode: "none"
        },
        columns: [
            {
                name: "id",
                dataField: "id",
                formItem: {
                    visible: false
                },
                alignment: "center",
                width: "10%",
            },
            {
                name: "title",
                dataField: "title",
                dataType: "string",
                alignment: "center",
            },

            {
                name: "done",
                dataField: "done",
                dataType: "boolean",
                alignment: "center",
                width: "10%",
            },
        ],
    }).dxDataGrid('instance');


})

