
    var obj = {
        "Electrician":['Improper Electrical Wiring','Installing electrical apparatus','Repair and replace equipments','Other'],
        "Plumber" : ["Improper Drainage","Leakage issues","Repair water supply lines",'Other'],
        "Carpenter": ["assa",'Other']
    }
    window.onload = function() {
  var wTypeSel = document.getElementById("wtype");
  var complaintSel = document.getElementById("complaint");
  for (var x in obj) {
    wTypeSel.options[wTypeSel.options.length] = new Option(x, x);
  }
  wTypeSel.onchange = function() {
    complaintSel.length=1;
    for (var y in obj[this.value]) {
        let ans = obj[this.value][y]
        complaintSel.options[complaintSel.options.length] = new Option(ans, ans);
    }
  }
}


burger=document.querySelector('.burger')
navbarm=document.querySelector('.navbarm')
navList=document.querySelector('.nav-listm')
rightNav=document.querySelector('.right-nav')

burger.addEventListener('click',()=>{
    navbarm.classList.toggle('h-nav-resp')
    navList.classList.toggle('vis-nav-resp')
    rightNav.classList.toggle('vis-nav-resp')
})

