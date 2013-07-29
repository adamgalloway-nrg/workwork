var timeEntryRowMarkup =
'<div class="entry-row">'+
	'<div class="row task-name-row">'+
		'<div class="large-14 columns">'+
			'<div class="task-name">{{taskName}}</div>'+
			'<div class="task-description">{{taskDescription}}</div>'+
		'</div>'+
		'<div class="large-2 columns text-right">'+
        	'<span class="delete" onclick="deletEntry(this, {{formId}});">[X]</span>'+
      	'</div>'+
        '<input id="id_form-{{formId}}-taskDefinitionId" name="form-{{formId}}-taskDefinitionId" type="hidden" value="{{taskDefinitionId}}">'+
		'<input id="id_form-{{formId}}-rowId" name="form-{{formId}}-rowId" type="hidden" value="">'+
	'</div>'+
	'<div class="row hours-row">'+
		'<div class="large-2 columns sun hours"><label class="show-for-small">Sun {{ sunTitle }}</label><input id="id_form-{{formId}}-sundayHours" name="form-{{formId}}-sundayHours" data-dirty="true" type="text" value="0"></div>'+
		'<div class="large-2 columns mon hours"><label class="show-for-small">Mon {{ monTitle }}</label><input id="id_form-{{formId}}-mondayHours" name="form-{{formId}}-mondayHours" data-dirty="true" type="text" value="0"></div>'+
		'<div class="large-2 columns tue hours"><label class="show-for-small">Tue {{ tueTitle }}</label><input id="id_form-{{formId}}-tuesdayHours" name="form-{{formId}}-tuesdayHours" data-dirty="true" type="text" value="0"></div>'+
		'<div class="large-2 columns wed hours"><label class="show-for-small">Wed {{ wedTitle }}</label><input id="id_form-{{formId}}-wednesdayHours" name="form-{{formId}}-wednesdayHours" data-dirty="true" type="text" value="0"></div>'+
		'<div class="large-2 columns thu hours"><label class="show-for-small">Thu {{ thuTitle }}</label><input id="id_form-{{formId}}-thursdayHours" name="form-{{formId}}-thursdayHours" data-dirty="true" type="text" value="0"></div>'+
		'<div class="large-2 columns fri hours"><label class="show-for-small">Fri {{ friTitle }}</label><input id="id_form-{{formId}}-fridayHours" name="form-{{formId}}-fridayHours" data-dirty="true" type="text" value="0"></div>'+
		'<div class="large-2 columns sat hours"><label class="show-for-small">Sat {{ satTitle }}</label><input id="id_form-{{formId}}-saturdayHours" name="form-{{formId}}-saturdayHours" data-dirty="true" type="text" value="0"></div>'+
		'<div class="large-2 columns row-total hide-for-small">0.00</div>'+
	'</div>'+
	'<div class="row comment-row">'+
		'<div class="large-14 columns comment">'+
    		'<input id="id_form-{{formId}}-comment" maxlength="500" name="form-{{formId}}-comment" data-dirty="true" placeholder="Comment" type="text" value="">'+
    	'</div>'+
	'</div>'+
'</div>';

var timeEntryRow = Hogan.compile(timeEntryRowMarkup);