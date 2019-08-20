import React from 'react';
import { API_ROOT } from '../../api-config';
import { withRouter } from 'react-router-dom';
import HighlightContainer from '../highlight/HighlightContainer';
import { Highlight } from '../highlight/Highlight';
import Model from '../Model'
import { truncateText } from '../DemoInput'
import 'rc-tabs/dist/rc-tabs.css'
import Tabs, { TabPane } from 'rc-tabs';
import TabContent from 'rc-tabs/lib/TabContent';
import ScrollableInkTabBar from 'rc-tabs/lib/ScrollableInkTabBar';
import Bibliography, {parseString} from 'bibliography'
import AMA from 'bibliography/AMA'

const apiUrl = () => `${API_ROOT}/predict/pampo`

const title = "Pampo";


var bib_article = "@article{Rocha2016PAMPOUP,\n"
        + "title={PAMPO: using pattern matching and pos-tagging for effective Named Entities recognition in Portuguese},\n"
        + "author={Conceiç{\~a}o Rocha and Al{\'i}pio M{\'a}rio Jorge and Roberta Sionara and Paula Brito and Carlos Pimenta and Solange Oliveira Rezende},\n"
        + "journal={CoRR},\n"
        + "year={2016},\n"
        + "volume={abs/1612.09535},\n"
        + "}";
    // Parse bibliography string
const bibliography = parseString(bib_article);



const description = (
  <span>
    <span>
        The method, named PAMPO (PAttern Matching and POs tagging based algorithm for NER), relies on flexible pattern matching, part-of-speech tagging and lexical-based rules. It was developed to process texts written in Portuguese, however it is potentially applicable to other languages as well.
    </span>
      <br/>
    <a href = "https://safe-basin-21244.herokuapp.com/home" target="_blank" rel="noopener noreferrer">
      {' '}Demo website{' '}
    </a>
    <br/>
    <a href = "https://github.com/LIAAD/py-pampo" target="_blank" rel="noopener noreferrer">{' '} Github {' '}</a>
  <br/>
  <pre style={{fontSize:"0.8em"}}>
  {bib_article} 
  </pre>
  </span>
)

const descriptionEllipsed = (
  <span>
    The method, named PAMPO...
  </span>


)

const fields = [
{name: "tabs", type: "TABS2",input:"opt_pampo"}]


const TokenSpan = ({ token ,named}) => {
    // Lookup table for entity style values:
    const entityLookup = {
      "WORK_OF_ART": {
        tooltip: "Named entity",
        color: "tan"
      },
    }

    const entity = token.entity;
    
        return (<Highlight label={"Named entity"} color={entityLookup['WORK_OF_ART'].color} tooltip={entityLookup['WORK_OF_ART'].tooltip}>{token} </Highlight>);
   
 
}


const Output = ({ responseData }) => {



    const {user,select}=responseData
    var callback = function(key){}

    let text1= user['text']
    let tokens1= user['tokens']

    let text2 = select['text'] 
    let tokens2 = select['tokens']
    let input_user=undefined
    let input_select=undefined
    let data1=[]


    if (text1!=undefined){
      {text1.map((token, i) => {
       if(tokens1.includes(token)){
        data1.push(<TokenSpan key={i} token={token} named={tokens1} />)
       }
       else{
        var string = token;
        string = string.split(" ");
        var stringArray = [];
        for(var i =0; i < string.length; i++){
          stringArray.push(string[i]);
          if(i != string.length-1){
            stringArray.push(" ");
          }
        }
            stringArray.map((tok,i)=> {data1.push(<p>{tok}</p>)})
       }
     }
      )}
        
      
      input_user=(<TabPane tab='Result for your text' key="1">
                                    <div>
                                    <HighlightContainer layout="bottom-labels">
                                    
                                      {data1.map((token, i) => token)} 
                                    
                                    </HighlightContainer>
                                    </div>
                                    </TabPane>)
    }
    let data2=[]
    if (text2!=undefined){
            {text2.map((token, i) => {
       if(tokens2.includes(token)){
        data2.push(<TokenSpan key={i} token={token} named={tokens2} />)
       }
       else{
        var string = token;
        string = string.split(" ");
        var stringArray = [];
        for(var i =0; i < string.length; i++){
          stringArray.push(string[i]);
          if(i != string.length-1){
            stringArray.push(" ");
          }
        }
            stringArray.map((tok,i)=> {data2.push(<p>{tok}</p>)})
       }
     }
      )}




      input_select=(<TabPane tab='Result for the demo text' key="2"> 
                                    <div>
                                    <HighlightContainer layout="bottom-labels">

                                      {data2.map((token, i) => token)} 

                                    </HighlightContainer>
                                    </div>
                                    </TabPane> )                   
    }
 

    return (

          <Tabs onChange={callback} renderTabBar={()=><ScrollableInkTabBar />} renderTabContent={()=><TabContent /> }>
                                    {input_user}
                                    {input_select}          
                                </Tabs>

    )
}

const examples = [].map(sentence => ({sentence, snippet: truncateText(sentence)}))



const modelProps = {apiUrl, title, description, descriptionEllipsed, fields, examples, Output}

export default withRouter(props => <Model {...props} {...modelProps}/>)