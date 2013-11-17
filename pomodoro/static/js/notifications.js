function notify(title, text, url) {
            var havePermission = window.webkitNotifications.checkPermission();
            if (havePermission == 0) {
                // 0 is PERMISSION_ALLOWED
                var notification = window.webkitNotifications.createNotification(
                        img,
                        title,
                        text
                );
                notification.onclick = function () {
                    notification.close();
                }
                notification.show();
            } else {
                window.webkitNotifications.requestPermission();
            }
        };

function notDoing(){
    notify("")

}