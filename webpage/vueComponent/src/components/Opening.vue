<!--HTML Formatting for front page-->
<template>
  <div class="row">
    <div class="col">
      <h1><u>How to</u></h1>
      <br>
      <p>Select your caption file</p>
      <p>Click the "Upload" Button</p>
      <p>This tool will show errors in your caption file that most other error detection software won't!</p>
    </div>
    <div class="col">
      <div class="container">
        <p><b>Choose your transcript file and click "Upload" to get started!</b></p>
        <form @submit.prevent="postFileToLambda">
          <div class="form-group">
            <input type="file" ref="userFile" @change="uploadFile">
          </div>
          <div>
            <button class="button" @click="$router.push('/analysis')"></button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
// Axios used for GET/POST requests with lambda endpoint
import axios from 'axios';

export default {
  name: "Opening",

  data(){
    return{
      transcript_file: null,
      lamdaResult: null,
      fileText: '',
      // Pass to POST request to return file name in Show.Vue
      fileName: ''
    };
  },

  methods:{

    // Get file from user
    uploadFile(){

      console.log('File selected')
      console.log(this.$refs.userFile.files[0])

      let transcript_file = this.$refs.userFile.files[0]

      if(!transcript_file || transcript_file.type !== 'text/plain') return;
      
      this.fileName = transcript_file.name;

      let reader = new FileReader();
    
      reader.readAsText(transcript_file, "UTF-8")
      reader.onload = event => {
        this.fileText = event.target.result; 
      }
      reader.onerror = event =>{
        console.error(event)
      } 
    },

    // read from file to post request to AWS Lamda
    postFileToLambda(){
      // CORS 'security pass' to allow for GET/POST requests with http endpoint
      const headers = {
        'Access-Control-Allow-Headers': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      }

      axios.post("https://f5lubai56d.execute-api.us-east-1.amazonaws.com/default/CapPageReturn", this.fileText, { headers })
      .then( (response) =>{
        console.log('Return Successful')
        console.log(response)
        console.log(this.fileText)
      })
      .catch(error => {
        console.error('Whoops, POST error', error.message);
      });
    }

  }
}
</script>

<style scoped>

.col {
  float: left;
  width: 50%;
  padding: 10px;
  height: 300px;
}

.row:after {
  content: "";
  display: table;
  clear: both;
}

* {
  box-sizing: border-box;
}

button {
  margin: 0;
  position: absolute;
  top: 30%;
  left: 55%;
  -ms-transform: translateY(-30%);
  transform: translateY(-20%);
  background-image: url("../assets/uploadButton.png");
  border-style: none;
  height: 54px;
  width: 150px;
  cursor: pointer;
}

</style>