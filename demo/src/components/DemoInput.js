import React from 'react';
import BeamSearch from './BeamSearch'
import {RadioGroup, Radio, Tooltip} from './Shared'
import ModelIntro from './ModelIntro'
import '../css/Button.css'
import Datepicker from './Calendar'
import AutocompleteExample from "./input_tags/components/autocomplete";
import 'react-tagsinput/react-tagsinput.css'
import ControlledTabs from './tabs.js'
import Tabs, { TabPane } from 'rc-tabs';
import TabContent from 'rc-tabs/lib/TabContent';
import ScrollableInkTabBar from 'rc-tabs/lib/ScrollableInkTabBar';
import 'rc-tabs/dist/rc-tabs.css'
import {opt,opt_pampo,opt_sen} from './input_text.js'
import 'rc-slider/assets/index.css';
import Slider from 'rc-slider';
import domains_PT from './demos/media.js'

const PATTERN_NON_WORD_CHAR = /\W/;
const PATTERN_WORD_CHAR = /\w/;
const ELLIPSIS = '…';
const EXAMPLE_NAME_SEPARATOR = '@@';
const DEFAULT_OPTION_GROUP = "DEFAULT_OPTION_GROUP";
/**
 * Truncates the provided text such that no more than limit characters are rendered and adds an
 * ellipsis upon truncation.  If the text is shorter than the provided limit, the full text is
 * returned.
 *
 * @param {string} text The text to truncate.
 * @param {number} limit The maximum number of characters to show.
 *
 * @return {string} the truncated text, or full text if it's shorter than the provided limit.
 */
const truncateText = (text, limit = 60) => {
    if (typeof limit !== 'number') {
      throw new Error('limit must be a number');
    }
    limit -= ELLIPSIS.length;
    if (text.length > limit) {
      while (
        limit > 1 &&
        (!PATTERN_WORD_CHAR.test(text[limit-1]) || !PATTERN_NON_WORD_CHAR.test(text[limit]))
      ) {
        limit -= 1;
      }
      if (limit === 1) {
        return text;
      } else {
        return text.substring(0, limit) + ELLIPSIS;
      }
    } else {
      return text;
    }
  };

let inp ={"opt":opt,"opt_pampo":opt_pampo,"opt_sen":opt_sen}

// Create a dropdown "snippet" for an example.
// If the example has a field called "snippet", use that;
// Otherwise, take the first field and truncate if necessary.
const makeSnippet = (example, fields, maxLen = 60) => {
    if (example.snippet) {
        return example.snippet
    } else {
        const fieldName = fields[0].name
        const snippet = example[fieldName]
        return truncateText(snippet, maxLen)
    }
}

class DemoInput extends React.Component {
    constructor(props) {
        super(props)

        const { examples, fields, inputState, runModel} = props
        if (!Array.isArray(examples[0])) {
          // TODO(mattg,jonb): Change this type to be [{"default": examples}]. Doing this requires
          // updating all of the other demos, and is probably best done by adding some kind of
          // Examples class, with a function like AddExample(data, optional group name).
          this.normalizedExamples = [[DEFAULT_OPTION_GROUP, examples]]
        } else {
          this.normalizedExamples = examples
        }
        this.state = inputState ? {...inputState} : {}
        // Populate state using (a copy of) provided values.



        this.domain_pt=domains_PT

        // What happens when you change the example dropdown
        this.handleExampleChange = e => {
            if (e.target.value !== "") {
                const { groupIndex, exampleIndex } = decodeExampleName(e.target.value)
                const example = this.normalizedExamples[groupIndex][1][exampleIndex]
                // Because the field names vary by model, we need to be indirect.
                let stateUpdate = {}

                // For each field,
                fields.forEach(({name}) => {
                    // if the chosen example has a value for that field,
                    if (example[name] !== undefined) {
                        // include it in the update.
                        stateUpdate[name] = example[name];
                    }
                })

                // And now pass the updates to setState.
                this.setState(stateUpdate)
            }
        }




        // What happens when you change an input. This works for text
        // inputs and also select inputs. The first argument is
        // the field name to update.
        this.handleInputChange = fieldName => e => {
            let stateUpdate = {}
            stateUpdate[fieldName] = e.target.value;
            this.setState(stateUpdate)
        }
        this.list=[]
        this.choose="Choose start date"
        this.value=""
        this.handleInputChangeCalendar = fieldName => date => {
            let stateUpdate = {}
            this.list.push(date)
            this.value=date
            if(this.list.length==1){
                
                this.choose="Now choose end date"
                stateUpdate[fieldName] = this.list;
                this.setState(stateUpdate)
            }
            else if (this.list.length==2){
                this.choose="Now select name domain"              
                stateUpdate[fieldName] = this.list;
                this.setState(stateUpdate)
            }
            else if (this.list.length>2){
                this.choose="You have already choose start and end date"
                this.list=[]
                stateUpdate[fieldName]={}
                this.setState(stateUpdate)
            }

            
        }
        
        this.list_tags2=[]
        this.handleInputChangeDomain = fieldName => tags => {
            let stateUpdate = {}
            this.list_tags2=tags
            stateUpdate[fieldName] = this.list_tags2;
            this.setState(stateUpdate)       
        }
        this.handlerText= fieldName => e => {

            let stateUpdate = {}
            stateUpdate["user"] = e.target.value;
            stateUpdate["active"] = "1";
            

            this.setState(stateUpdate)
        }
        this.state["slider1"]=3
        this.handlerSlide1=fieldName => value => {
            let stateUpdate = {}
            stateUpdate["slider1"] = value;
            this.setState(stateUpdate)
        }
        this.state["slider2"]=20
        this.handlerSlide2=fieldName => value => {
            let stateUpdate = {}
            stateUpdate["slider2"] = value;
            this.setState(stateUpdate)
        }
        this.handlerActive=fieldName => value => {
            let stateUpdate = {}
            stateUpdate["active"] = value
            this.setState(stateUpdate)
        }
        this.handlerSelect= fieldName => e => {
            let stateUpdate = {}
            stateUpdate["select"] = e.target.value;
            stateUpdate["active"] = "2";
            this.setState(stateUpdate) 
            this.state["val"]= e.target.value.substr(3);       
            
        }
        this.handlerSelect2= fieldName => e => {
            let stateUpdate = {}
            stateUpdate["select"] = e.target.value;
            this.state["active"]="2"
            this.setState(stateUpdate)           
            this.state["val"]= e.target.value;       
            
        }

        this.handleRadioInputChange = fieldName => value => {
            let stateUpdate = {}
            stateUpdate["radio1"] = value;
            this.setState(stateUpdate)
        }

        this.handleRadioInputChange2 = fieldName => value => {
            let stateUpdate = {}
            stateUpdate["radio2"] = value;
            console.log(value)
            if(value=="all"){
                this.list_tags2=this.domain_pt
            }
            else{
                this.list_tags2=[]
            }
            stateUpdate["domain"] = this.list_tags2;
            this.setState(stateUpdate)
        }

        // Handler that runs the model if 'Enter' is pressed.
        this.runOnEnter = e => {
            if (e.key === 'Enter') {
                e.preventDefault();
                e.stopPropagation();
                runModel(this.cleanInputs())
            }
        }

        // Some of the inputs (e.g. interactive beam search)
        // depend on the previous outputs, so when we do a new run
        // we need to clear them out.
        this.cleanInputs = () => {
            let inputs = {...this.state}

            fields.forEach((field) => {
                (field.dependentInputs || []).forEach((name) => {
                    delete inputs[name]
                })
            })
            return inputs
        }
    }

    render() {

        var callback = function(key){}

        const { title, description, descriptionEllipsed, fields, selectedModel, outputState, responseData, inputState } = this.props

        // Only enable running the model if every required field has a value.
        const canRun = fields.every(field => field.optional || this.state[field.name] || this.state["user"] || this.state["select"])

        // Fields that are inputs only.
        const inputs = []

        // Fields that are both inputs and outputs (e.g. beam search). These will be
        // rendered below the RUN button.
        const inputOutputs = []

        fields.forEach((field, idx) => {
            // The HTML id for this input:
            const inputId = `input--${selectedModel}-${field.name}`
            const label = field.label ? <label htmlFor={`#${inputId}`}>{field.label}</label> : null

            let input = null;

            switch (field.type) {
                case "TEXT_AREA":
                case "TEXT_INPUT":
                    // Both text area and input have the exact same properties.
                    const props = {
                        onChange: this.handleInputChange(field.name),
                        onKeyDown: canRun ? this.runOnEnter : undefined,
                        id: inputId,
                        type: "text",
                        required: "true",
                        autoFocus: idx === 0,
                        placeholder: field.placeholder || "",
                        value: this.state[field.name],
                        disabled: outputState === "working",
                        maxLength: field.maxLength || (field.type === "TEXT_INPUT" ? 1000 : 100000)
                    }

                    input = field.type === "TEXT_AREA" ? <textarea {...props}/> : <input {...props}/>
                    break

                case "SELECT":
                    input = (
                        // If we have no value for this select, use the first option.
                        <select value={this.state[field.name] || field.options[0]}
                                onChange={this.handleInputChange(field.name)}
                                disabled={outputState === "working"}>
                            {
                                field.options.map((value) => (
                                    <option key={value} value={value}>{value}</option>
                                ))
                            }
                        </select>
                    )
                    break

                case "BEAM_SEARCH":
                    if (outputState !== "working") {
                        const { best_action_sequence, choices } = responseData || {}
                        const runSequenceModel = (extraState) => this.props.runModel({...this.state, ...extraState}, true)

                        input = <BeamSearch inputState={inputState}
                                            bestActionSequence={best_action_sequence}
                                            choices={choices}
                                            runSequenceModel={runSequenceModel}/>
                    }
                    break

                case "RADIO":
                    input = (
                        // If we have no value for this select, use the first option.
                        <RadioGroup
                            name={inputId}
                            selectedValue={this.state[field.name] || (field.options[0] && field.options[0].name)}
                            onChange={this.handleRadioInputChange(field.name)}
                            disabled={outputState === "working"}>
                            {
                                field.options.map((opt) => (
                                    <label key={opt.name} data-tip={opt.desc}>
                                        <Radio value={opt.name}/>{opt.name}
                                    </label>
                                ))
                            }
                      </RadioGroup>
                    )
                    break
                case "TABS":

                    const wrapperStyle = { width: 400, margin: 50 };


                    input = (    <Tabs activeKey={this.state["active"]==undefined? "1":this.state["active"]} onChange={this.handlerActive("active")} renderTabBar={()=><ScrollableInkTabBar />} renderTabContent={()=><TabContent />}>
                                    <TabPane tab='Free Input' key="1"><textarea value={this.state["user"]} onChange={this.handlerText("user")} /></TabPane>
                                    <TabPane tab='Demo Text' key="2"> <br/>
                                    <select value={this.value_select} onChange={this.handlerSelect("select")}>  
                                        {
                                            Object.keys(inp[field.input]).map((key, index) => ( 
                                            <option key={key} value={inp[field.input][key]}>{key}</option>
                                            ))
                                        }
                                     </select>
                                     <textarea value={this.state["val"]}/>
                                    <div style={wrapperStyle}>
                                        <p>Inform max ngram size</p>
                                        <Slider min={1} max={4} defaultValue={1} value={this.state["slider1"]} onChange={this.handlerSlide1("slider")} marks={{1: 1, 2: 2, 3: 3, 4: 4 }} step={null} />
                                        
                                    </div>
                                    <div style={wrapperStyle}>
                                        <p>Inform number of keywords</p>
                                    <Slider min={10} max={60}  value={this.state["slider2"]} onChange={this.handlerSlide2("slider")} marks={{10: 10, 20: 20, 30: 30, 40: 40,50:50,60:60 }} step={null} />
                                    </div>
                                    </TabPane>
                                    
                                </Tabs>)
                    break
                    case "TABS2":


                    input = (    <Tabs defaultActiveKey={this.state["active"]==undefined? "1":this.state["active"]} onChange={this.handlerActive("active")} renderTabBar={()=><ScrollableInkTabBar />} renderTabContent={()=><TabContent />}>
                                    <TabPane tab='Free Input' key="1"><textarea value={this.state["user"]} onChange={this.handlerText("user")} /></TabPane>
                                    <TabPane tab='Demo Text' key="2"> <br/>
                                    <select value={this.value_select} onChange={this.handlerSelect("select")}>  
                                        {
                                            Object.keys(inp[field.input]).map((key, index) => ( 
                                            <option key={key} value={inp[field.input][key]}>{key}</option>
                                            ))
                                        }
                                     </select>
                                     <textarea value={this.state["val"]}/>
                                    </TabPane>
                                    
                                </Tabs>)
                    break
                case "CALENDAR":

                    input = (<Tabs defaultActiveKey={"1"} onChange={callback} renderTabBar={()=><ScrollableInkTabBar />} renderTabContent={()=><TabContent />}>
                                 <TabPane tab='Calendar' key="1">
                                    <Datepicker alert={this.choose}  realValue={this.list} value={this.value} onChange={this.handleInputChangeCalendar(field.name)}  />
                                 </TabPane>
                                 <TabPane tab='Other' key="2">
                                 <RadioGroup
                                    name={"radio1"}
                                    
                                    onChange={this.handleRadioInputChange("radio1")}
                                    disabled={outputState === "working"}>
                            
                               
                                    <label key={"five"} data-tip={"five"}>
                                        <Radio value={"five"}/>{"Last 5 years"}
                                    </label>
                                      <label key={"ten"} data-tip={"ten"}>
                                        <Radio value={"ten"}/>{"Last 10 years"}
                                    </label>
                                      <label key={"fifteen"} data-tip={"fifteen"}>
                                        <Radio value={"fifteen"}/>{"Last 15 years"}
                                    </label>
                                
                            
                      </RadioGroup>
                                 </TabPane>
                                </Tabs>
                                )
                    break
                case "DOMAIN":

                    input= (   <div> <br/>
                                <RadioGroup
                                    name={"radio2"}                            
                                    onChange={this.handleRadioInputChange2("radio2")}
                                    selectedValue={this.state["radio2"]}
                                    disabled={outputState === "working"}>                                                          
                                    <label key={"all"} data-tip={"all"}>
                                        <Radio value={"all"}/>{"Select All Domains"}
                                    </label>
                                    <label key={"cancel"} data-tip={"cancel"}>
                                        <Radio value={"cancel"}/>{"Cancel Selection"}
                                    </label>
                                    </RadioGroup>
                                    <br/>
                                    <AutocompleteExample value={this.list_tags2} onChange={this.handleInputChangeDomain("domain")} />                          
                                </div>
                            )

                    break
                case "TEXT":
                    input=<textarea value={this.state[field.name]} onChange={this.handleInputChange(field.name)} />
                    break
                default:
                    console.error("unknown field type: " + field.type)
            }
            let div = (
                <div className="form__field" key={field.name}>
                {label}
                {input}
                </div>)

            // By default we assume a field is just an input,
            // unless it has the ``inputOutput`` attribute set.
            if (field.inputOutput) {
                inputOutputs.push(div)
            } else {
                inputs.push(div)
            }
        })
                let out=(<div className="model__content answer">
                <ModelIntro title={title} description={description} descriptionEllipsed={descriptionEllipsed}/>
                <div className="form__instructions"> 
                </div>
                {inputs}
                <div className="form__field form__field--btn">
                    <button
                     id="input--mc-submit"
                     type="button"
                     disabled={!canRun || outputState === "working"}
                     className="btn btn--icon-disclosure"
                     onClick={ () => this.props.runModel(this.cleanInputs()) }>Run
                        <svg>
                            <use xlinkHref="#icon__disclosure"></use>
                        </svg>
                    </button>
                </div>
                {inputOutputs}
                <Tooltip multiline/>
            </div>)
            
        if(fields[0].type=="PRESENTATION"){
            out=(<div className="model__content answer">
                <ModelIntro title={title} description={description} descriptionEllipsed={descriptionEllipsed}/>
                <div className="form__instructions"> 
                </div></div>)
        }


        return out
    }
}

function OptionGroup(exampleInfo, groupIndex, fields) {
  const exampleType = exampleInfo[0]
  const examples = exampleInfo[1]
  if (!exampleType || exampleType === DEFAULT_OPTION_GROUP) {
      return RenderOptions(examples, groupIndex, fields)
  } else {
      return (
          <optgroup label={exampleType}>
              {RenderOptions(examples, groupIndex, fields)}
          </optgroup>
      )
  }
}

function RenderOptions(examples, groupIndex, fields) {
    return examples.map((example, exampleIndex) => {
        const encodedName = encodeExampleName(groupIndex, exampleIndex)
        return (
            <option value={encodedName} key={encodedName}>{makeSnippet(example, fields)}</option>
        )
    })
}

function encodeExampleName(groupIndex, exampleIndex) {
  return groupIndex + EXAMPLE_NAME_SEPARATOR + exampleIndex
}

function decodeExampleName(name) {
  const parts = name.split(EXAMPLE_NAME_SEPARATOR)
  return {
    groupIndex: parts.length ? parts[0] : undefined,
    exampleIndex: parts.length > 0 ? parts[1] : undefined,
  }
}

export { DemoInput as default, truncateText }
