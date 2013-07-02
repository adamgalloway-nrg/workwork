var timeEntryRowMarkup =
'<div class="entry-row">'+
	'<div class="row task-name-row">'+
		'<div class="large-14 columns">'+
			'<div class="task-name">{{taskName}}</div>'+
			'<div class="task-description">{{taskDescription}}</div>'+
		'</div>'+
        '<input id="id_form-{{formId}}-taskDefinitionId" name="form-{{formId}}-taskDefinitionId" type="hidden" value="{{taskDefinitionId}}">'+
		'<input id="id_form-{{formId}}-rowId" name="form-{{formId}}-rowId" type="hidden" value="">'+
	'</div>'+
	'<div class="row hours-row">'+
		'<div class="large-2 columns sun hours"><input id="id_form-{{formId}}-sundayHours" name="form-{{formId}}-sundayHours" type="text" value="0"></div>'+
		'<div class="large-2 columns mon hours"><input id="id_form-{{formId}}-mondayHours" name="form-{{formId}}-mondayHours" type="text" value="0"></div>'+
		'<div class="large-2 columns tue hours"><input id="id_form-{{formId}}-tuesdayHours" name="form-{{formId}}-tuesdayHours" type="text" value="0"></div>'+
		'<div class="large-2 columns wed hours"><input id="id_form-{{formId}}-wednesdayHours" name="form-{{formId}}-wednesdayHours" type="text" value="0"></div>'+
		'<div class="large-2 columns thu hours"><input id="id_form-{{formId}}-thursdayHours" name="form-{{formId}}-thursdayHours" type="text" value="0"></div>'+
		'<div class="large-2 columns fri hours"><input id="id_form-{{formId}}-fridayHours" name="form-{{formId}}-fridayHours" type="text" value="0"></div>'+
		'<div class="large-2 columns sat hours"><input id="id_form-{{formId}}-saturdayHours" name="form-{{formId}}-saturdayHours" type="text" value="0"></div>'+
		'<div class="large-2 columns row-total">0.00</div>'+
	'</div>'+
	'<div class="row comment-row">'+
		'<div class="large-14 columns comment">'+
    		'<input id="id_form-{{formId}}-comment" maxlength="500" name="form-{{formId}}-comment" placeholder="Comment" type="text" value="">'+
    	'</div>'+
	'</div>'+
'</div>';

var timeEntryRow = Hogan.compile(timeEntryRowMarkup);