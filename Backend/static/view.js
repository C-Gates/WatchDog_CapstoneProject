function create_view() {

    var view_name = document.getElementById('view_name');

    var checkboxes = document.getElementsByName("checkbox");
    console.log(checkboxes.length);

    const checked_details = [];

    for(var i = 0; i < checkboxes.length; i++) {
        if(checkboxes[i].checked == true) {
            checked_details.push(checkboxes[i].value);
        }
    }

    console.log(checked_details);
    console.log(view_name.value);

    const view_entry = {"view_name" : view_name.value, "details" : checked_details};

    write_view(view_entry);

    function write_view(entry) {
        fetch(`${window.origin}/watchlist/create_view`, {
            method: "POST",
            credentials : "include",
            body: JSON.stringify(entry),
            cache: "no-cache",
            headers : new Headers({
                "content-type" : "application/json"
            })
        })
        .then(function (response) {
            if (response.status !== 200) {
                console.log(`Error ${response.status}`);
                return;
            }
            else {
                location.reload();
            }
        });
    }

};
