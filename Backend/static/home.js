
highNas();
activeNas();
highAsx();
activeAsx();

function highNas(){
   fetch(`${window.origin}/homepage/highestNas`)
   .then(function (response) {
       if (response.status !== 200) {
           console.log(`Error ${response.status}`);
           return data;
       }
       response.json(). then(function (data) {
           var highN = ``;
           var lowN = ``;
           for (item in data){
               //console.log(data[item]);
                if (data[item] > 0){
                        var highN = highN + `<a href ="${window.origin}/NASDAQ/${item}">
                            <div class="col-sm-2 info">
                                <div class="arrow-gain"><i class="fas fa-angle-up"></i></div>
                                <p class="gainnum">${data[item]}%<br></p><p class="gain">${item}</p>
                                
                            </div>
                        </a>`
                        
                }
                else {
                    var lowN = lowN  + `<a href ="${window.origin}/NASDAQ/${item}">
                        <div class="col-sm-2 info">
                            
                            <div class="arrow-loss"><i class="fas fa-angle-down"></i></div>
                            <p class="lossnum">${data[item]}%<br></p><p class="loss">${item}</p>
                            
                        </div>
                    </a>`
                    
                }
                $('#highNas').html(highN);
                $('#lowNas').html(lowN);
                
           }
       })
   });
}

function activeNas() {
    fetch(`${window.origin}/homepage/activeNas`)
    .then(function (response) {
        if (response.status !== 200) {
            console.log(`Error ${response.status}`);
            return data;
        }
        response.json(). then(function (data) {
            var activeN = ``;
            for (item in data){
                //console.log(data[item]);
                if (data[item] > 0){
                        var activeN = activeN + `<a href ="${window.origin}/NASDAQ/${item}">
                            <div class="col-sm-2 info">
                                <div class="arrow-gain"><i class="fas fa-angle-up"></i></div>
                                <p class="gainnum">${data[item]}%<br></p><p class="gain">${item}</p>
                                
                            </div>
                        </a>`
                        
                }
                else {
                    var activeN = activeN  + `<a href ="${window.origin}/NASDAQ/${item}">
                        <div class="col-sm-2 info">
                            
                            <div class="arrow-loss"><i class="fas fa-angle-down"></i></div>
                            <p class="lossnum">${data[item]}%<br></p><p class="loss">${item}</p>
                            
                        </div>
                    </a>`
                    
                }
                $('#moveNas').html(activeN);
                
            }
        })
    });
}

function highAsx() {
    fetch(`${window.origin}/homepage/highestAsx`)
    .then(function (response) {
        if (response.status !== 200) {
            console.log(`Error ${response.status}`);
            return data;
        }
        response.json(). then(function (data) {
            var highA = ``;
            var lowA = ``;
            for (item in data){
                //console.log(data[item]);
                 if (data[item] > 0){
                         var highA = highA + `<a href ="${window.origin}/ASX/${item}">
                             <div class="col-sm-2 info">
                                 <div class="arrow-gain"><i class="fas fa-angle-up"></i></div>
                                 <p class="gainnum">${data[item]}%<br></p><p class="gain">${item}</p>
                                 
                             </div>
                         </a>`
                         
                 }
                 else {
                     var lowA = lowA  + `<a href ="${window.origin}/ASX/${item}">
                         <div class="col-sm-2 info">
                             <div class="arrow-loss"><i class="fas fa-angle-down"></i></div>
                             <p class="lossnum">${data[item]}%<br></p><p class="loss">${item}</p>
                             
                         </div>
                     </a>`
                     
                 }
                 $('#highAsx').html(highA);
                 $('#lowAsx').html(lowA);
                 
            }
        })
    });
}



function activeAsx() {
    fetch(`${window.origin}/homepage/activeAsx`)
    .then(function (response) {
        if (response.status !== 200) {
            console.log(`Error ${response.status}`);
            return data;
        }
        response.json(). then(function (data) {
            var activeA = ``;
            for (item in data){
                //console.log(data[item]);
                if (data[item] > 0){
                        var activeA = activeA + `<a href ="${window.origin}/ASX/${item}">
                            <div class="col-sm-2 info">
                                <div class="arrow-gain"><i class="fas fa-angle-up"></i></div>
                                <p class="gainnum">${data[item]}%<br></p><p class="gain">${item}</p>
                                
                            </div>
                        </a>`
                        
                }
                else {
                    var activeA = activeA  + `<a href ="${window.origin}/ASX/${item}">
                        <div class="col-sm-2 info">
                            <div class="arrow-loss"><i class="fas fa-angle-down"></i></div>
                            <p class="lossnum">${data[item]}%<br></p><p class="loss">${item}</p>
                            
                        </div>
                    </a>`
                    
                }
                $('#moveAsx').html(activeA);
                
            }
        })
    });
}


/*
fetch(`${window.origin}/homepage/highestNas`)
.then(function (response) {
    if (response.status !== 200) {
        console.log(`Error ${response.status}`);
        return data;
    }
    response.json(). then(function (data) {
        console.log(data);
        const highN = data;
    })
});*/