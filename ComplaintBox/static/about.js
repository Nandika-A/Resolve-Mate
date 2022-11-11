burger=document.querySelector('.burger')
navbarm=document.querySelector('.navbarm')
navList=document.querySelector('.nav-listm')
rightNav=document.querySelector('.right-nav')

burger.addEventListener('click',()=>{
    navbarm.classList.toggle('h-nav-resp')
    navList.classList.toggle('vis-nav-resp')
    rightNav.classList.toggle('vis-nav-resp')
})
