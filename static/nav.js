var main=document.querySelector('main')
if(main.offsetHeight>=700){
    document.getElementsByTagName('footer')[0].style.position='relative';
    document.querySelector('.downloads').style.position='relative';
}
else{
    document.getElementsByTagName('footer')[0].style.position='fixed';
    document.querySelector('.downloads').style.position='fixed';
}