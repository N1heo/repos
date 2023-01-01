function loadData() {  
    fetch('https://api.capybara-api.xyz/v1/image/random')
    .then(response => response.json())
    .then(json => {
		document.getElementById("imageCapy").src = json.storage_url;
    })
    
}

function loadPage() {
    $("#background").animate({}, 800, function() {
        $("#clickbtn").animate({height: "200px", width: "200px"}, 850, function() {
        $("#clickbtn").animate({fontSize: "30px"}, 850, function() {
        $("#score").animate({fontSize: "25px"}, 850, function() {
        })
        })
        })
    })
    }

function loadAll(){
    loadPage();
    loadData();
}
