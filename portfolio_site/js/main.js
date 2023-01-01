var score = 0;

const btn = document.getElementById("clickbtn")

let index = 0;

const colors = ['#24c6dc', '#29b4d7', '#2da3d1', '#3194cc','#3587c7','#397ac2','#3c6fbd','#3f65b7','#425cb2','#4455ad','#464ea7','#4948a2','#514a9d', '#4948a2', '#464ea7', '#4455ad', '#425cb2', '#3f65b7', '#3c6fbd', '#397ac2', '#3587c7', '#3194cc', '#2da3d1', '#29b4d7', '#24c6dc'];

btn.addEventListener('click', function onClick() {
  btn.style.backgroundColor = colors[index];
  btn.style.color = 'white';

  index = index >= colors.length - 1 ? 0 : index + 1;
});

function clickBtn() {
  const btn = document.getElementById("clickbtn")
  score++;
  console.log(score);
  document.getElementsByClassName("score_text_js")[0].firstChild.data = "Clicks: " + score;
  ("#click")
  if (score == 20){
    window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', '_blank');
    btn.style.backgroundImage = "url(https://upload.wikimedia.org/wikipedia/ru/thumb/7/78/Trollface.svg/1200px-Trollface.svg.png)";
    var element = document.getElementById("button_text");
    element.innerHTML = "Ooops..."
  }
}

