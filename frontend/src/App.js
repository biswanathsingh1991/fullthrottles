import React, { Component } from 'react';
import axios from "axios";
import './App.css';


class App extends Component {

  state={
    word:"",
    resPonse:[],
  }


  getWords = (word) =>{
    axios({
      method: 'GET',
      url: "http://127.0.0.1:8000/api/?search="+word, //Development
      headers: {
        "Content-Type": 'application/json',
        'Accept': 'application/json',
      },
    }).then(res=>{
      if (res.status===200){
        console.log(res)
        this.setState({
          ...this.state,
          resPonse:res.data,
        })
      }
    }).catch(err=>{
      console.error(err.response)
    })
  }

  onWordChange = (e) =>{
    this.setState({
      ...this.state,
      word:e.target.value
    })
    if(e.target.value){
      this.getWords(e.target.value)
    }
  }
  

  render() {
    

    return(
      <div >
        <label htmlFor="word-search">Word</label>
        <input type="text" value={this.props.word} name="word" id="word-search" onChange={this.onWordChange}/>
        {
          this.state.word ?
          <ol>
            {
              this.state.resPonse.length>0?
              this.state.resPonse.map((u, index)=>{
                return(
                  <li key={index}>
                  <span>{u.word}</span> <span>{u.count}</span>
                </li>
                )
              })
              : <li> Loading .......</li>
            }
          </ol>
          :null
        }
      </div>
    )
  }
}

  
  

export default App;
