let page=0;
let keyword='';
let Fetching = false;

async function fetchAttractions(){
    try{
        const response=await fetch(`/api/attractions?page=${page}&keyword=${keyword}`);
        const data=await response.json();
        if (data) {
            addAttraction(data.data);
            if (data.nextPage===null){
                window.removeEventListener('scroll', handleScroll);
            } else {
                page=data.nextPage;
            }
        } 
    }catch (error) {
        console.error('景點資料獲取失敗:', error);
    }
}

function addAttraction(attractions) {
    const Container=document.getElementById('attractions-container');
    if (!attractions || attractions.length === 0) {
        console.error('查無景點資料');
        return;
    }
    for (let i=0; i < attractions.length; i++) {
        const attraction=attractions[i];
        const attractionExists=Container.querySelector(`[data-id="${attraction.id}"]`);
        if (!attractionExists) {

            // each-attraction
            const eachAttraction=document.createElement('div');
            eachAttraction.classList.add('index-each-attraction');
            eachAttraction.setAttribute('data-id', attraction.id);
            
            // attraction-imgContainer
            const imgContainer=document.createElement('div');
            imgContainer.classList.add('index-attraction-imgContainer');
            
            // img
            const img=document.createElement('img');
            img.src=attraction.images[0];
            img.alt=attraction.name;

            imgContainer.appendChild(img);
            eachAttraction.appendChild(imgContainer);
        
            // attraction-name
            const name=document.createElement('div');
            name.classList.add('index-attraction-name', 'font-body-bold16-white');
            name.setAttribute('data-id', attraction.id);
            imgContainer.appendChild(name);

            //link 
            const link = document.createElement('a');
            link.href = `/attraction/${attraction.id}`;
            link.textContent=attraction.name;
            name.appendChild(link);
                     
            // attraction-info
            const info=document.createElement('div');
            info.classList.add('index-attraction-info');
            
            const mrt=document.createElement('div');
            mrt.classList.add('index-info-mrt','font-body-med16-gray');
            mrt.textContent=attraction.mrt;
            
            const cat=document.createElement('div');
            cat.classList.add('index-info-cat', 'font-body-med16-gray');
            cat.textContent=attraction.cat;
        
            info.appendChild(mrt);
            info.appendChild(cat);
            eachAttraction.appendChild(info);


            Container.appendChild(eachAttraction);
        };
    }
}    


function handleScroll(){
    if (Fetching) return; 

    const scrollTop=(document.documentElement && document.documentElement.scrollTop) || document.body.scrollTop;
    const scrollHeight=(document.documentElement && document.documentElement.scrollHeight) || document.body.scrollHeight;
    const clientHeight=document.documentElement.clientHeight || window.innerHeight;
    const scrolledToBottom=Math.ceil(scrollTop + clientHeight) >= scrollHeight;

    if (scrolledToBottom) {
        Fetching=true; 
        fetchAttractions().then(() => {
            Fetching=false; 
        });
    }
}

function handleSearchSubmit(event) {
    event.preventDefault(); 
    keyword=document.getElementById('keyword').value.trim(); 
    page=0; 
    const container=document.getElementById('attractions-container');
    container.innerHTML=''; 
    window.removeEventListener('scroll', handleScroll);
    fetchAttractions(); 
    window.addEventListener('scroll', handleScroll);
}

window.addEventListener('DOMContentLoaded', fetchAttractions);
window.addEventListener('scroll', handleScroll);
document.getElementById('searchForm').addEventListener('submit', handleSearchSubmit);

