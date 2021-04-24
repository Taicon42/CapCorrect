<template>
  <div class="flex-container">
    <!--Left column containing normal text from file-->
    <div class="col1" style="background-color: white">
      <!--Button returns user to starting screen for file upload-->
      <button class="cButton" @click="$router.push('/')" style="float: right"></button>
      <h2 style="background-color: lightgray">{{ fileName }}</h2>
      <div v-for="item in apiData" v-bind:key="item.id" class="d-flex flex-row">
        <div class="p-2">
          <span > {{item.timestamp + item.err_text}}</span>
        </div>
      </div>
    </div>
    <!--Right column containing error information-->
    <div class="col2" style="background-color: gray">
      <h2 style="background-color: lightgray">Possible Errors</h2>
      <!-- Creates a tab containing error information for each unique id-->
      <div v-for="item in apiData" v-bind:key="item.id" class="d-flex flex-row">
        <div data-cy='err_info_tab' class="p-2" >{{item.timestamp}}
          <p v-if="item.has_error">Incorrect sentence: {{ item.err_text }}</p>
          <p v-if="item.has_error">Sugguestion(s): {{ item.sugguestions }}</p>          
          <p v-else style="background-color: #42b983" data-cy='no_error'>No errors detected</p>
          <button data-cy='err_toggle' class="collapse_button" @click="toggle_showDetails(item)">Show Errors</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
export default {
  name: "Show",
  data() {
    return{
      text_One:"\n\nSo this is just an example of some text to show...\n\n",
      fileName: "TranscriptFileName",
      hover: false, 
      apiData: undefined
    };

  },

  // Do the following upon page creation
  mounted(){
      // Calls to static return lamda functions
      // To be replaced with new dynamic return
      axios.get("https://f5lubai56d.execute-api.us-east-1.amazonaws.com/default/CapPageReturn")
            .then((response) => {
              this.apiData = response.data,
              console.log(response.data),
              this.text_display(response)
              });
  },

  methods:{

      // Toggle whether or not to show error details
      toggle_showDetails(item){
        item.has_error = !item.has_error
      }
  }
}
</script>

<style scoped>

*{
  box-sizing: border-box;
  border-style: solid;
}
.col1{
  width:60%;
  height: 600px;
  padding:10px;
  float:left;
  border-style:solid;
}

.col2{
  width:40%;
  height: 600px;
  padding:10px;
  float:left;
  border-style: solid;
}

.d-flex.flex-row{
  border-style: none;
  padding-bottom: 10px;
}

[contenteditable] {
  outline: 0px solid transparent;
}

.span{
  outline: 0px solid transparent;
}
.info {
  border-style: none;
  border-radius: 15px;
  text-align: center;
  padding: 0 15px;
  overflow: hidden;
  display: block;
}

.row:after {
  clear:both;
  display:table;
  content:"";
  height:auto;
}

.cButton{
  background-image: url('../assets/closeButton.png');
  border-style: none;
  height: 45px;
  width: 119px;
  flex-wrap: wrap;
  cursor: pointer;
}

h2 {
  font-size: 1.3em;
}

.container {
  border-radius:15px;
  border:3px solid black;
  background-color: -moz-default-background-color;
  color:white;
}

#textArea:hover ~ container{
  background-color: #ff6148;
}

textarea{
  background-color: white;
  color: black;
  min-height: 10%;
  width: -moz-fit-content;
  width: fit-content;
  resize: none;
}

.collapse_button{
  background-color: #ff6148;
  border-style: none;
  text-align: left;
  cursor: pointer;
  outline: none;
}



</style>