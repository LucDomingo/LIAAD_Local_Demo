import React from 'react';
import '../css/Pane.css';
import '../css/model.css';
import '../css/passage.css';
import { StageSpinner } from "react-spinners-kit";

import logo from './eye.png'

/*******************************************************************************
  <ResultDisplay /> Component
*******************************************************************************/

class ResultDisplay extends React.Component {

    render() {
      const { resultPane, outputState } = this.props;

      const placeholderTemplate = (message) => {
        return (
          <div className="placeholder">
            <div className="placeholder__content">
                <img  style={{maxWidth:'10%'}} src={logo} alt="Logo" />
              {message !== "" ? (
                <p>{message}</p>
              ) : null}
            </div>
          </div>
        );
      }

      let outputContent;
      switch (outputState) {
        case "working":
          outputContent = ( <div className="placeholder">
            <div className="placeholder__content"><StageSpinner
                size={60}
                color="#0f4e66"
                loading="true"
            /></div>
          </div>)
          break;
        case "received":
          outputContent = this.props.children;
          break;
        case "error":
          outputContent = placeholderTemplate("Something went wrong. Please try again.");
          break;
        default:
          // outputState = "empty"
          outputContent = placeholderTemplate("Run model to view results");
      }

      return (
        <div className={`pane__${resultPane} model__output ${outputState !== "received" ? "model__output--empty" : ""}`}>
          <div className="pane__thumb"></div>
          {outputContent}
        </div>
      );
    }
}


/*******************************************************************************
  <PaneRight /> Component
*******************************************************************************/

export class PaneRight extends React.Component {
    render() {
      const { outputState } = this.props;

      return (
        <ResultDisplay resultPane="right" outputState={outputState}>
          {this.props.children}
        </ResultDisplay>
      )
    }
}

/*******************************************************************************
  <PaneBottom /> Component
*******************************************************************************/

export class PaneBottom extends React.Component {
  render() {
    const { outputState } = this.props;

    return (
      <ResultDisplay resultPane="bottom" outputState={outputState}>
        {this.props.children}
      </ResultDisplay>
    )
  }
}


/*******************************************************************************
<PaneLeft /> Component
*******************************************************************************/

export class PaneLeft extends React.Component {

    render () {
      return (
        <div className="pane__left model__input">
          {this.props.children}
        </div>
      );
    }
}

/*******************************************************************************
<PaneTop /> Component
*******************************************************************************/

export class PaneTop extends React.Component {

  render () {
    return (
      <div className="pane__top model__input">
        {this.props.children}
      </div>
    );
  }
}