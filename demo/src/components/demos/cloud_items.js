import React from 'react';
import './style_cloud.css';

const CloudItem = (props) => (
    <div { ...props } className="tag-item-wrapper">
        <div>
            { props.text }
        </div>
        <div className="tag-item-tooltip">
            HOVERED!
        </div>
    </div>
);

export default CloudItem;
