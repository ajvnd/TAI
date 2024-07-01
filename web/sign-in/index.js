$(function () {

    const sign_in_form = $("#form").dxForm({
        formData: {
            email: "",
            password: ""
        },
        items: [{
            dataField: "email",
            label: {text: "Email", alignment: "left"},
            editorOptions: {placeholder: "Enter email"}
        }, {
            dataField: "password",
            label: {text: "Password", alignment: "left"},
            visible: true,
            editorOptions: {
                placeholder: "Enter password",
                mode: "password"
            }
        }, {
            itemType: "button",
            horizontalAlignment: "right",
            buttonOptions: {
                text: "Sign In",
                type: "default",
                onClick(e) {
                }
            }
        }]
    }).dxForm("instance");

    $(".forgot-password").on("click", (e) => {
        let visible = sign_in_form.itemOption("password").visible;

        const $sign_in_form_title = $(".sign-in-form-title");

        if (!visible) {
            $sign_in_form_title.text("Sign In")
            $(e.currentTarget).text("Forgot Password")
            sign_in_form.itemOption("password", "visible", true)
        } else {
            $sign_in_form_title.text("Forgot Password")
            $(e.currentTarget).text("Sign in")
            sign_in_form.itemOption("password", "visible", false)
        }
    })

})