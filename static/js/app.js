
    /* data route */

    var url = "/names";
    
  Plotly.d3.json(url, function(error, response) {
    var info=response.Names
    console.log(info);
    for(var i = 0; i < info.length; i++){
      var select = document.getElementById("selDataset");
      datas=info[i];
    var opt=document.createElement("option");
      opt.value=datas;
      opt.innerHTML=datas;
      document.getElementById("selDataset").append(opt)
    }
   
  })

  function buildplot(sample){
 
    var Datapie=[{
        values:sampleData["Sample Values"].slice(0,10),
        labels:sampleData["Otu_ID"].slice(0,10),
        type:"pie"
    }]
    var pie_sel = document.getElementById('pie');
            Plotly.plot(pie_sel, Datapie)
 
  } 
  function getData(sample, callback) {
    // Use a request to grab the json data needed for all charts
    Plotly.d3.json(`/samples/${sample}`, function(error, sampleData) {
        if (error) return console.warn(error);
        callback(sampleData)
    })
  }
  