#! /bin/bash

# Get COVID-19 data from web
wget -O raw_us_data.dat https://github.com/nytimes/covid-19-data/raw/master/us.csv
wget -O tmp.dat https://github.com/nytimes/covid-19-data/raw/master/us-states.csv
wget -O ny_curve.dat https://github.com/nychealth/coronavirus-data/raw/master/case-hosp-death.csv

# Removes 3rd field from raw_state_data.dat
awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' x=3 < tmp.dat > raw_state_data.dat

clear 
echo ""
echo "                COVID-19 DATA ANALYSIS BY JUDAH PAUL                      "
echo "-----------------------------------------------------------------------"
echo ""
echo "Enter a state postal code corresponding to your state of interest"
echo "(cumulative infections / deaths), i.e. 'GA' for Georgia or " 
echo -n "enter 'US' for United States plot or simply ENTER to quit: "

read state

case $state in
	
	AL | al)
		sed '2,${/Alabama/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
		       	x=2 < tmp.dat > data.dat		
		;;
	AK | ak)
		sed '2,${/Alaska/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	AZ | az)
		sed '2,${/Arizona/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	AR | ar)
		sed '2,${/Arkansas/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	CA | ca)
		sed '2,${/California/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	CO | co)
		sed '2,${/Colorodo/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	CT | ct)
		sed '2,${/Connecticut/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	DE | de)
		sed '2,${/Delaware/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	DC | dc)
		sed '2,${/District of Columbia/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	FL | fl)
		sed '2,${/Florida/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	GA | ga)
		sed '2,${/Georgia/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	HI | hi)
		sed '2,${/Hawaii/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	ID | id)
		sed '2,${/Idaho/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	IL | il)
		sed '2,${/Illinois/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	IN )
		sed '2,${/Indiana/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	IA | ia)
		sed '2,${/Iowa/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	KS | ks)
		sed '2,${/Kansas/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	KY | ky)
		sed '2,${/Kentucky/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	LA | LO | la | lo)
		sed '2,${/Louisiana/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	ME | me)
		sed '2,${/Maine/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	MD | md)
		sed '2,${/Maryland/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	MA | ma)
		sed '2,${/Massachusetts/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	MI | mi)
		sed '2,${/Michigan/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	MN | mn)
		sed '2,${/Minnesota/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	MS | ms)
		sed '2,${/Mississippi/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	MO | mo)
		sed '2,${/Missouri/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	MT | mt)
		sed '2,${/Montana/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	NE | ne)
		sed '2,${/Nebraska/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	NV | nv)
		sed '2,${/Nevada/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	NH | nh)
		sed '2,${/New Hampshire/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	NJ | nj)
		sed '2,${/New Jersey/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	NM | nm)
		sed '2,${/New Mexico/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	NY | ny)
		sed '2,${/New York/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	NC | nc)
		sed '2,${/North Carolina/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	ND | nd)
		sed '2,${/North Dakota/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	OH | oh)
		sed '2,${/Ohio/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	OK | ok)
		sed '2,${/Oklahoma/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	OR | or)
		sed '2,${/Oregon/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	PA | pa)
		sed '2,${/Pennsylvania/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	RI | ri)
		sed '2,${/Rhode Island/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	SC | sc)
		sed '2,${/South Carolina/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	SD | sd)
		sed '2,${/South Dakota/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	TN | tn)
		sed '2,${/Tennessee/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	TX | tx)
		sed '2,${/Texas/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	UT | ut)
		sed '2,${/Utah/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	VT | vt)
		sed '2,${/Vermont/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	VA | va)
		sed '2,${/Virginia/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	WA | wa)
		sed '2,${/Washington/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	WV | wv)
		sed '2,${/West Virginia/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	WI | wi)
		sed '2,${/Wisconsin/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	WY | wy)
		sed '2,${/Wyoming/!d}' < raw_state_data.dat > tmp.dat
		# Removes 2nd field from raw_state_data.dat
		awk -F, '{for(i=1;i<=NF;i++)if(i!=x)f=f?f FS $i:$i;print f;f=""}' \
			x=2 < tmp.dat > data.dat		
		;;
	US | us)
		mv raw_us_data.dat data.dat
		;;
	*)
		;;
	esac

if [[ $state = "" ]]
then
	echo ""
	echo "Alternatively, you can view the current model of New York's"
	echo "daily increase in infections / hospitalizations / deaths"
	echo -n "from COVID-19 'y' or 'n': "
	read var
	
	if [[ "$var" = "y" ]]
	then
		echo ""
		echo "Keep Calm: A gif should pop up in about 30 seconds"
		gnuplot -p gnuplot_noncumm.p
	fi
else
	echo ""
	gnuplot -p gnuplot_cumm.p
	clear
	echo "Keep Calm: A gif should pop up in about 30 seconds"
fi

rm tmp.dat
xviewer graph.gif &

exit 0
