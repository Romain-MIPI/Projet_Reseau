
window.onload = () => {
    let input = document.getElementById("a");
    //let btncheck;
    let flow_data;
    let list = document.getElementById("flow"); 
    
  









    let filter = document.getElementById("filter");

    eel.expose(check_if_filter)
    function check_if_filter(){
        if (filter.value == '') {
            alert("filter_v")
            document.getElementById("filter").style = "color:rgb(0, 0, 0);";
            return 0;}
        else{
            return filter.value;
        }}

        //TODO filter set to 0
    filter.onchange = async (ev) =>{   
       let t = await eel.validate_filter()()
       if(t == 0){   
            document.getElementById("filter").style = "color:rgb(255, 0, 0);";
            }
        else{
            document.getElementById("filter").style = "color:rgb(25, 200, 65);";
            

            let i = 0
            eel.expose(pass_i)
            function pass_i(){
                return i
            }
            
            while (await eel.filter_output()() != "end_of_list"){
                let data = await eel.filter_output()();
                alert(data)
                i = i + 1;
            }
        
        
        
        }
       

    }
/*

    async function get_data(){
    let d = await eel.load_data()();
    //alert(d)
    return d;}

    function print_list(data){
        data.forEach((dir)=>{
            dir.forEach((item)=>{
                let li = document.createElement("li");
                li.innerText = item;
                list.appendChild(li);})
            }
          );
        }
    
    eel.expose(load_a);
    function load_a(){
        return j;
    }
  
    let j = 1;
    input.onchange = async (ev) => {
    flow_data = await get_data();
    document.getElementById("clicked").innerText = "yes";
    print_list(flow_data);
    
    let res;
    res  = await eel.double()()
    //eel.checkval();
    j = res;
    eel.checkval();
    document.getElementById("var").innerText = res;
    document.getElementById("double").innerText = res;
}*/
}