$(function () {
    const SERVICE_URL = "http://127.0.0.1:8000/tasks";

    $("#tasksGrid").dxDataGrid({
        dataSource: new DevExpress.data.CustomStore({
            key: "id",
            load: function () {
                return $.getJSON(SERVICE_URL);
            },
            insert: function (values) {
                return $.ajax({
                    url: SERVICE_URL,
                    method: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(values)
                });
            },
            update: (key, values) => {
                return $.ajax({
                    url: `${SERVICE_URL}/${encodeURIComponent(key)}`,
                    method: "PUT",
                    contentType: "application/json",
                    data: JSON.stringify(values)
                });
            },
            remove: (key) => {
                return $.ajax({
                    url: `${SERVICE_URL}/${encodeURIComponent(key)}`,
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
            {
                name: "id",
                dataField: "id",
                formItem: {
                    visible: false
                }
            },
            {
                name: "title",
                dataField: "title",
                dataType: "string",
            },
            {
                name: "is_completed",
                dataField: "is_completed",
                dataType: "boolean",
            },
            {
                name: "due_date",
                dataField: "due_date",
                dataType: "datetime",
            },
        ]
    });

    let drawer = $("#settings").dxDrawer({
        height: 400,
        opened: true,
        openedStateMode: 'shrink',
        template() {
            const $list = $('<div>').width(200).addClass('panel-list dx-theme-typography-background-color');

            return $list.dxList({
                dataSource: [
                    {id: 1, text: 'help', icon: 'help'},
                    {id: 2, text: 'Settings', icon: 'preferences'}
                ],
                hoverStateEnabled: false,
                focusStateEnabled: false,
                activeStateEnabled: false,
            });
        },
    }).dxDrawer('instance');

    $('#toolbar').dxToolbar({
        items: [{
            widget: 'dxButton',
            location: 'before',
            options: {
                icon: 'menu',
                stylingMode: 'text',
                onClick() {
                    drawer.toggle();
                },
            },
        }],
    });
})