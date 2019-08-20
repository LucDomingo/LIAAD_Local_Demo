import React from 'react';
import { API_ROOT } from '../../api-config';
import { withRouter } from 'react-router-dom';
import HighlightContainer from '../highlight/HighlightContainer';
import { Highlight } from '../highlight/Highlight';
import Model from '../Model'
import { truncateText } from '../DemoInput'
import WordCloud from 'react-d3-cloud';
import 'rc-tabs/dist/rc-tabs.css'
import Tabs, { TabPane } from 'rc-tabs';
import TabContent from 'rc-tabs/lib/TabContent';
import ScrollableInkTabBar from 'rc-tabs/lib/ScrollableInkTabBar';

const apiUrl = () => `${API_ROOT}/predict/yake`

const title = "YAKE! Collection-independent Automatic Keyword Extractor";


const fontSizeMapper = word => 1/Math.sqrt(word.value)*10;
const rotate = word => word.value % 45;


var bib_article = "@article{\n"
        + "title={A Text Feature Based Automatic Keyword Extraction Method for Single Documents.},\n"
        + "author={Campos, R., & Mangaravite, V., & Pasquali, A., & Jorge, A., & Nunes, C., & Jatowt, A. },\n"
        + "journal={In Gabriella Pasi et al. (Eds.), Lecture Notes in Computer Science - Advances in Information Retrieval - 40th European Conference on Information Retrieval (ECIR'18).Grenoble, France. March 26 – 29},\n"
        + "year={2018},\n"
        + "volume={Vol. 10772(2018), pp. 684 - 691},\n"
        + "}";
var bib_article2 = "@article{\n"
        + "title={YAKE! Collection-independent Automatic Keyword Extractor.},\n"
        + "author={Campos, R., & Mangaravite, V., & Pasquali, A., & Jorge, A., & Nunes, C., & Jatowt, A.},\n"
        + "journal={In Gabriella Pasi et al. (Eds.), Lecture Notes in Computer Science - Advances in Information Retrieval - 40th European Conference on Information Retrieval (ECIR'18).},\n"
        + "year={2018},\n"
        + "volume={Vol. 10772(2018), pp. 806 - 810},\n"
        + "}";


const description = (
  <span>
    <span>
        Extracting keywords from texts has become a challenge for individuals and organizations as the information grows in complexity and size. The need to automate this task so that texts can be processed in a timely and adequate manner has led to the emergence of automatic keyword extraction tools. Despite the advances, there is a clear lack of multilingual online tools to automatically extract keywords from single documents. In this paper, we present Yake!, a novel feature-based system for multi-lingual keyword extraction, which supports texts of different sizes, domain or languages. Unlike most of the systems, Yake! does not rely on dictionaries nor thesauri, neither is trained against any corpora. Instead, we follow an unsupervised approach which builds upon features extracted from the text, making it thus applicable to documents written in different languages without the need for further knowledge. This can be beneficial for a large number of tasks and a plethora of situations where the access to training corpora is either limited or restricted. In this demo, we offer an easy to use, interactive session, where users from both academia and industry can try our system, either by using a sample document or by introducing their own text. As an add-on, we compare our extracted keywords against the output produced by the IBM Natural Language Understanding and Rake system. This will enable users to understand the distinctions between the three approaches. 
    </span>
    <br/>
    <a href = "http://yake.inesctec.pt/" target="_blank" rel="noopener noreferrer">
      {' '}Demo website{' '}
    </a>
    <br/>
    <a href = "https://github.com/LIAAD/yake" target="_blank" rel="noopener noreferrer">{' '} Github {' '}</a>
    <br/>
     <br/>
  <pre style={{fontSize:"0.8em"}}>
  {bib_article} 
  </pre>
       <br/>
  <pre style={{fontSize:"0.8em"}}>
  {bib_article2} 
  </pre>
  </span>

)

const descriptionEllipsed = (
  <span>
    Extracting keywords from texts has become a challenge for individuals and organizations as the information grows in complexity and size...
  </span>
)

const fields = [
    {name: "tabs", type: "TABS",input:"opt"}
]
const TokenSpan = ({ key,token ,named,namedup}) => {
    // Lookup table for entity style values:
    const entityLookup = {
      "PER": {
        tooltip: "Person",
        color: "pink"
      },
      "LOC": {
        tooltip: "Location",
        color: "green"
      },
      "ORG": {
        tooltip: "Organization",
        color: "blue"
      },
      "MISC": {
        tooltip: "Miscellaneous",
        color: "gray"
      },
      "PERSON": {
        tooltip: "Person",
        color: "pink"
      },
      "CARDINAL": {
        tooltip: "Cardinal Number",
        color: "orange"
      },
      "EVENT": {
        tooltip: "Event",
        color: "green"
      },
      "DATE": {
        tooltip: "Date",
        color: "fuchsia"
      },
      "FAC": {
        tooltip: "Facility",
        color: "cobalt"
      },
      "GPE": {
        tooltip: "Country/City/State",
        color: "teal"
      },
      "LANGUAGE": {
        tooltip: "Language",
        color: "red"
      },
      "LAW": {
        tooltip: "Law",
        color: "brown"
      },
      // LOC - see above
      "MONEY": {
        tooltip: "Monetary Value",
        color: "orange"
      },
      "NORP": {
        tooltip: "Nationalities, Religious/Political Groups",
        color: "green"
      },
      "ORDINAL": {
        tooltip: "Ordinal Value",
        color: "orange"
      },
      // ORG - see above.
      "PERCENT": {
        tooltip: "Percentage",
        color: "orange"
      },
      "PRODUCT": {
        tooltip: "Product",
        color: "purple"
      },
      "QUANTITY": {
        tooltip: "Quantity",
        color: "orange"
      },
      "TIME": {
        tooltip: "Time",
        color: "fuchsia"
      },
      "WORK_OF_ART": {
        tooltip: "Named entity",
        color: "tan"
      },
    }


        let i= namedup.indexOf(token.toUpperCase())
        entityLookup['NORP'].tooltip=named[1][i]
        return (<Highlight label={"keyword"} color={entityLookup['NORP'].color} tooltip={entityLookup['NORP'].tooltip}>{token} </Highlight>);
}

const Output = ({ responseData }) => {
 
    const { user, select,original1,original2 } = responseData
    var callback = function(key){}


    const data1 = [];
    const data2 = [];

    const dt2=[[],[]];
    const dt1=[[],[]];

    let t1=[]
    let t2=[]

    let input_user=undefined
    let input_select=undefined





    if(user!="No text given"){
        {user.map((token, i) => { data1.push({"text":token[0],"value":token[1]});dt1[0].push(token[0]);dt1[1].push(token[1])})}
        let namedup=[]
        dt1[0].map((tok,i)=>{namedup.push(tok.toUpperCase())})
        let tmp=[]

        {original1.map((token, i) =>{
          if(namedup.includes(token.toUpperCase())){
            t1.push(<TokenSpan token={token} named={dt1} namedup={namedup} />)
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
            stringArray.map((tok,i)=> {t1.push(<p>{tok}</p>)})
          }
            
          
        })
        }
        input_user=(
                         <Tabs onChange={callback} renderTabBar={()=><ScrollableInkTabBar />} renderTabContent={()=><TabContent />}>
                              <TabPane tab='Word Cloud' key="1">
                                     <WordCloud     data={data1}
                                        fontSizeMapper={fontSizeMapper}
                                      rotate={rotate}/>
                                </TabPane>
                                <TabPane tab='Highlighted Text' key="2">
                                <div className="model__content model__content--ner-output">
                                 <div className="form__field"> 
                                     <div><HighlightContainer layout="bottom-labels">
                                    
                                       {t1.map((token, i) => token)} 
                                    
                                    </HighlightContainer></div></div></div>
                                </TabPane>
                                <TabPane tab='Keywords list' key="3">
                                          <div className="model__content model__content--ner-output">
          <div className="form__field"> 
                                {dt1[0].map((token,i)=><p>{token}</p>)}
                                </div></div>
                                </TabPane>

                                
                            </Tabs>)
    }
    if(select!="No demo text given"){
      
      {select.map((token, i) => { data2.push({"text":token[0],"value":token[1]});dt2[0].push(token[0]);dt2[1].push(token[1])})}
      let namedup=[]
      dt2[0].map((tok,i)=>{namedup.push(tok.toUpperCase())})
      let tmp=[]
               
          {original2.map((token, i) =>{
          if(namedup.includes(token.toUpperCase())){
            t2.push(<TokenSpan token={token} named={dt2} namedup={namedup} />)
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
            stringArray.map((tok,i)=> {t2.push(<p>{tok}</p>)})
          }
            
          
        })
        }


      input_select=(
                         <Tabs onChange={callback} renderTabBar={()=><ScrollableInkTabBar />} renderTabContent={()=><TabContent />}>
                              <TabPane tab='Word Cloud' key="1">
                                     <WordCloud     data={data2}
                                        fontSizeMapper={fontSizeMapper}
                                      rotate={rotate}/>
                                </TabPane>
                                <TabPane tab='Highlighted Text' key="2">
                                     <div><HighlightContainer layout="bottom-labels">
                                    
                                       {t2.map((token, i) => token)} 
                                    
                                    </HighlightContainer></div>
                                </TabPane>
                                <TabPane tab='Keywords list' key="3">
                                          <div className="model__content model__content--ner-output">
          <div className="form__field"> 
                                {dt2[0].map((token,i)=><p>{token}</p>)}
                                </div></div>
                                </TabPane>

                                
                            </Tabs>)
    }
    let input_1
    let input_2
    let out
    let active="1"
    if(input_user!=undefined && input_select!=undefined){
          input_1=(                  <TabPane tab='Result for your text' key="1"> 
                              {input_user}
                       </TabPane> )
          input_2=(<TabPane tab='Result for the sample text' key="2"> 
                              {input_select}
                       </TabPane> )
          out=(      <Tabs onChange={callback} renderTabBar={()=><ScrollableInkTabBar />} renderTabContent={()=><TabContent />}>
                      {input_1}
                      {input_2}
 
      </Tabs>)
  
    }
    else if(input_user!=undefined && input_select==undefined){
                input_1=(                  <TabPane tab='Result for your text' key="1"> 
                              {input_user}
                       </TabPane> )
          
          out=(      <Tabs onChange={callback} renderTabBar={()=><ScrollableInkTabBar />} renderTabContent={()=><TabContent />}>
                      {input_1}
                     
 
      </Tabs>)
    }
   else if(input_user==undefined && input_select!=undefined){
                 input_2=(<TabPane tab='Result for the sample text' key="2"> 
                              {input_select}
                       </TabPane> )
          
          out=(      <Tabs onChange={callback} renderTabBar={()=><ScrollableInkTabBar />} renderTabContent={()=><TabContent />}>
                      {input_2}
                     </Tabs>)
    }
    return (out)




    
}



const examples = [
  ].map(sentence => ({sentence, snippet: truncateText(sentence)}))



const modelProps = {apiUrl, title, description, descriptionEllipsed,examples, fields, Output}

export default withRouter(props => <Model {...props} {...modelProps}/>)