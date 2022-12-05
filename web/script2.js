
window.onload = () => {
    let input = document.getElementById("a");
    //let btncheck;
    let flow_data;

    load_flow();







    let filter = document.getElementById("filter");

    eel.expose(check_if_filter)
    function check_if_filter(){
        if (filter.value == '') {
           
            document.getElementById("filter").style = "color:rgb(0, 0, 0);";
            return 0;}
        else{
            return filter.value;
        }}

        //TODO filter set to 0


    filter.onchange = async (ev) =>{ 
        load_flow()} 
        
    async function load_flow(){
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

            function contains(a, obj) {
                for (var i = 0; i < a.length; i++) {
                    if(JSON.stringify(a[i]) === JSON.stringify(obj)){
                        return true;
                    }
                }
                return false;
            }

            function index(a, obj){
                for (var i = 0; i < a.length; i++) {
                    if(JSON.stringify(a[i]) === JSON.stringify(obj)){
                        return i;
                    }
                }
                return false;
            }

            let ip_array = [];
            while (await eel.filter_output()() != "end_of_list"){

               
                let data = await eel.filter_output()();
                //alert(data)
                if(data != 0){
                    if(contains(ip_array, data['ip']['src']) == 0){
                        ip_array.push(data['ip']['src']);

                    };
                    if(contains(ip_array, data['ip']['dst']) == 0){
                        ip_array.push(data['ip']['dst']);
                    };

                    let row = document.getElementById("flows").insertRow(-1);
                    let cell1 = row.insertCell(0);
                    let cell2 = row.insertCell(1);
                    let cell3 = row.insertCell(2);
                    let cell4 = row.insertCell(3);
                    
                    cell1.innerHTML = i;
                    //cell1.style = style="background-color:#909090;"
                    
                    let src = index(ip_array, data['ip']['src'])
                    let dst = index(ip_array, data['ip']['dst']);
                    let start_pad = '';
                    start_pad += " ".repeat(Math.min(src, dst));
                    
                    let middle_pad;
                    if(dst < src){
                        
                        let dist = (((src - dst)*19) + (((src - dst) -1)*16))
                        middle_pad = "<" + "-".repeat(dist);alert(middle_pad)
                    }
                    if(dst > src){
                        let dist = (((dst-src)*19) + (((dst-src) -1)*16))
                        middle_pad = '-'.repeat(dist) + ">";} 
                    let ip_msg = start_pad + ip_array[Math.min(src, dst)] + middle_pad + ip_array[Math.max(src, dst)];
                    
                    cell2.innerHTML = ip_msg
                    cell3.innerHTML = data['tcp']['type'];
                    cell4.innerHTML = data['http']['comm'];
                    
                }
                
                i = i + 1;
            }
            let ip_s = '';
            
            for(var j = 0; j < ip_array.length-1;j++){
                ip_s += ip_array[j] + " ".repeat(20);}
            ip_s += ip_array[ip_array.length -1]
            document.getElementById("showip").innerText = ip_s



            function generateTable(table, ipa) {
                alert("test")
                alert(ipa)
                let row = table.insertRow();
                for (let element of ipa) {
                    
                  
                  //for (key in element) {
                    let cell = row.insertCell();
                    let text = document.createTextNode(element);
                    cell.appendChild(text);
                 // }
                }
              }
        
              //let table = document.querySelector("table");
              //generateTable(table, ip_array)
        
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