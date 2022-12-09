
window.onload = () => {
    let file = document.getElementById("file");

    eel.expose(pass_file)
    function pass_file(){
        return file.value
    }
    load_flow();

    file.onchange = async (ev) =>{
        load_flow();
    }
    let output_array= [];
    let file_count = 1;
    let filter = document.getElementById("filter");
    let btn = document.getElementById("reset_button");
    filter.onchange = async (ev) =>{ 
        load_flow()} 
    btn.onclick = async (ev) =>{ 
        load_flow()} 


    eel.expose(pass_output_strings)
    function pass_output_strings(){
        return output_array;
    }

    eel.expose(pass_file_count)
    function pass_file_count(){return file_count;}


    eel.expose(check_if_filter)
    function check_if_filter(){
        if (filter.value == '') {
            document.getElementById("filter").style = "color:rgb(0, 0, 0);";
            return 0;}
        else{
            return filter.value;
        }}
    


    function DeleteRows() {
        let table = document.getElementById("flows")
        var rowCount = table.rows.length;
        for (var i = rowCount - 1; i > 0; i--) {
            table.deleteRow(i);
        }
    }

    async function load_flow(){
       let t = await eel.validate_filter()();
       DeleteRows()
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
            let data_array = [];
            while (await eel.filter_output()() != "end_of_list"){

                let data = await eel.filter_output()();
                if(data !== 0){
                    if (data['ip'] !== null){
                        if (data['tcp'] !== null){
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
                    let cell5 = row.insertCell(4);
                    let cell6 = row.insertCell(5);
                    
                    cell1.innerHTML = i;                    
                    
                    let src = index(ip_array, data['ip']['src'])
                    let dst = index(ip_array, data['ip']['dst']);
                    let start_pad = '';
                    start_pad = " ".repeat(15* Math.min(src, dst) + 20*Math.min(src, dst));
                    
                    let middle_pad;
                    let ip_msg;
                    
                    if(dst < src){
                        
                        let dist = (((src - dst)*20) + (((src - dst) -1)*15)-5)
                        let pad = 15 - data['tcp']['dst'][0].length
                        
                        middle_pad = "  <" + "-".repeat(dist + pad) + "  ";
                        ip_msg = start_pad + data['tcp']['dst'][0] + middle_pad + data['tcp']['src'][0];
                    }
                    if(dst > src){
                        let dist = (((dst-src)*20) + (((dst-src) -1)*15)-5)
                        let pad = 15 - data['tcp']['src'][0].length
                        
                        middle_pad = "  " + '-'.repeat(dist + pad) + ">  ";
                        
                        //alert(src)
                        //alert(dst)
                        //alert(ip_array)
                    
                    ip_msg = start_pad + data['tcp']['src'][0] + middle_pad + data['tcp']['dst'][0];}
                    
                    cell2.innerHTML = ip_msg
                    cell3.innerHTML = data['tcp']['type'];
                    cell4.innerHTML = data['tcp']['seq_num']    
                    cell5.innerHTML = data['tcp']['ack_num'];
                    cell6.innerHTML = data['http']['comm']; 
                    let s = "\n";
                    let line = i.toString() + s + ip_msg + s +  data['tcp']['type'] + s + data['tcp']['seq_num'] + s + data['tcp']['ack_num'] + data['http']['comm'][0].replace(/(\r\n|\n|\r)/gm, "\t") + "_end_of_line";
                    data_array.push(line.toString());
                }}}
                
                i = i + 1;
            }
            let ip_s = ''
            for(var j = 0; j < ip_array.length-1;j++){
                ip_s += ip_array[j] + " ".repeat(20+ (15-ip_array[j][0].length));}
            ip_s += ip_array[ip_array.length -1]
            document.getElementById("showip").innerText = ip_s
            
            let s =  "\n"
            output_array.push('#' + s + ip_s +s+ "type TCP" +s+ '# Seq' +s+ '# ACK' +s+ 'Commentaire'+ s+ "_end_of_line,")
            output_array += data_array
        }
        eel.save_to_file()
        count += 1

    }
}