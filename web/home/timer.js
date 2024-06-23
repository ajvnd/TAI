const Default_Pomodoro_time = 25;
const $timerValue = $("<div>").addClass("timer-value dx-theme-text-color");

function get_timer(on_finish) {
    return $(".focus-popup").dxPopup({
        dragEnabled: false,
        showTitle: false,
        contentTemplate: (container) => {
            container.addClass("custom-popup").append($timerValue);
            start_timer(Default_Pomodoro_time * 1, on_finish)
        }
    }).dxPopup('instance');
}

function start_timer(current_time, on_finish) {
    function update_timer() {
        var minutes = Math.floor(current_time / 60);
        var seconds = current_time % 60;

        // Format seconds to always have two digits
        var formattedSeconds = seconds < 10 ? "0" + seconds : seconds;

        $timerValue.text(minutes + ":" + formattedSeconds);

        if (current_time > 0) {
            current_time--;
            setTimeout(update_timer, 1000);
        } else {
            $timerValue.text("Time's up!");
            on_finish()
        }
    }

    update_timer()
}


