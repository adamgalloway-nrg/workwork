package com.nrgedge.jasper;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Map;

import net.sf.jasperreports.engine.JRDataSource;
import net.sf.jasperreports.engine.JRDataset;
import net.sf.jasperreports.engine.JRException;
import net.sf.jasperreports.engine.JRValueParameter;
import net.sf.jasperreports.engine.JasperReportsContext;
import net.sf.jasperreports.engine.data.JRBeanCollectionDataSource;
import net.sf.jasperreports.engine.query.AbstractQueryExecuterFactory;
import net.sf.jasperreports.engine.query.JRQueryExecuter;

public class WeekIdQueryExecutorFactory extends AbstractQueryExecuterFactory {

	public class WeekIdQueryExecutor implements JRQueryExecuter {
		
		public class WeekIdRow {
			
			public Integer id;
			
			public WeekIdRow(Integer id) {
				this.id = id;
			}

			public Integer getId() {
				return id;
			}

			public void setId(Integer id) {
				this.id = id;
			}
		}

		private Integer start;
		private Integer end;
		
		private SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMW");
		
		public WeekIdQueryExecutor(Integer start, Integer end) {
			if (end < start) {
				this.start = end;
				this.end = start;
			} else {
				this.start = start;
				this.end = end;
			}
		}
		
		@Override
		public JRDataSource createDatasource() throws JRException {

			final Calendar cal = Calendar.getInstance();
			
	        final List<WeekIdRow> list = new ArrayList<WeekIdRow>();
	        
	        list.add(new WeekIdRow(start));
	        
			try {
				final Date startDate = sdf.parse(String.valueOf(start));
				cal.setTime(startDate);
				cal.add(Calendar.DATE, 7);
				
				Integer weekId = Integer.valueOf(sdf.format(cal.getTime()));
				
				while (weekId < end) {
					list.add(new WeekIdRow(weekId));
					
					cal.add(Calendar.DATE, 7);
					weekId = Integer.valueOf(sdf.format(cal.getTime()));
				}
				
			} catch (ParseException e) {
				e.printStackTrace();
			}
	        
			if (end != null && !end.equals(start)) {
				list.add(new WeekIdRow(end));
			}
			
	        
	        return new JRBeanCollectionDataSource(list);

		}

		@Override
		public void close() {
		}

		@Override
		public boolean cancelQuery() throws JRException {
			return true;
		}
		
	}
	
	@Override
	public Object[] getBuiltinParameters() {
		return null;
	}

	@Override
	public JRQueryExecuter createQueryExecuter(
			JasperReportsContext jasperReportsContext, JRDataset dataset,
			Map<String, ? extends JRValueParameter> parameters)
			throws JRException {
		
		Integer start = (Integer)parameters.get("start_date_query").getValue();
		Integer end = (Integer)parameters.get("end_date_query").getValue();
		

		return new WeekIdQueryExecutor(start, end);
	}

	@Override
	public boolean supportsQueryParameterType(String className) {
		return true;
	}



}
