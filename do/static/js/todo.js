/**
 * Created with PyCharm.
 * User: stefanotranquillini
 * Date: 10/15/13
 * Time: 2:35 PM
 * To change this template use File | Settings | File Templates.
 */
$("addtask").keypress(function(event) {
    if (event.which == 13) {
        event.preventDefault();
        $("form").submit();
    }
});