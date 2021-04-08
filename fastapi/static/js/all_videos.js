function toggle_hidden(id) {
    var classVal = document.getElementById(id).getAttribute("class");
    if (classVal.includes("hide_cls")) {
        classVal = classVal.replace("hide_cls", "");

    }
    else {
        classVal = classVal.concat("hide_cls");

    }
    document.getElementById(id).setAttribute("class", classVal);

}
function addtag(name_id, tag_name) {
    $.ajax({
        url: "/api/v1/add_tag",
        type: "post",
        data: { "name_id": name_id, "tag_name": tag_name },
        dataType: "json",
        success: function (data) {
            console.log(data)
        }

    })
}

function outerlink(path) {
    return "http://" + window.location.hostname + ":8000/" + path,
}



var navito = (url) => {
    window.open("http://" + window.location.hostname + ":8000/" + url, "videos");

};
var minHeight = 225;
var minWidth = 400;


function img_size_suite() {
    document.querySelectorAll("img.poster").forEach(element => {
        if (window.innerWidth < 400) {
            minWidth = window.innerHeight - 40;
            minHeight = minWidth * (225 / 400)
        }
        element.width = minWidth;
        element.height = minHeight;
    });
}


window.onresize = img_size_suite
window.onload = img_size_suite

