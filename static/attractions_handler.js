let page=0;
let keyword='';


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
        } else {
            console.error('查無景點資料');
        }

    }catch (error) {
        console.error('景點資料獲取失敗:', error);
    }
}

function addAttraction(attractions) {
    const Container=document.getElementById('attractions-container');
    for (let i=0; i < attractions.length; i++) {
        const attraction=attractions[i];
        const attractionExists=Container.querySelector(`[data-id="${attraction.id}"]`);
        if (!attractionExists) {
            // each-attraction
            const eachAttraction=document.createElement('div');
            eachAttraction.classList.add('each-attraction');
            eachAttraction.setAttribute('data-id', attraction.id);
            
            // attraction-imgContainer
            const imgContainer=document.createElement('div');
            imgContainer.classList.add('attraction-imgContainer');
            
            // img
            const img=document.createElement('img');
            img.src=attraction.images[0];
            img.alt=attraction.name;
        
            // attraction-name
            const name=document.createElement('div');
            name.classList.add('attraction-name', 'font-body-bold16-white');
            name.textContent=attraction.name;

            imgContainer.appendChild(name);
            imgContainer.appendChild(img);
            eachAttraction.appendChild(imgContainer);

            // attraction-info
            const info=document.createElement('div');
            info.classList.add('attraction-info');
            
            const mrt=document.createElement('div');
            mrt.classList.add('info-mrt','font-body-med16-gray');
            mrt.textContent=attraction.mrt;
            
            const cat=document.createElement('div');
            cat.classList.add('info-cat', 'font-body-med16-gray');
            cat.textContent=attraction.cat;
        
            info.appendChild(mrt);
            info.appendChild(cat);
            eachAttraction.appendChild(info);

            Container.appendChild(eachAttraction);
        };
    }    
}

function handleScroll(){
    const scrollTop=(document.documentElement && document.documentElement.scrollTop) || document.body.scrollTop;
    const scrollHeight=(document.documentElement && document.documentElement.scrollHeight) || document.body.scrollHeight;
    const clientHeight=document.documentElement.clientHeight || window.innerHeight;
    const scrolledToBottom=Math.ceil(scrollTop + clientHeight) >= scrollHeight;

    if (scrolledToBottom) {
        fetchAttractions();
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

