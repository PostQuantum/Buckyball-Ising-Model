#include <stdio.h>
#include <math.h>
#include "mf.h"
#include <gsl/gsl_integration.h>

//****************************the functions are listed below**********
double func1 (double y, double T)  //The self-consistent equation f(y)=0
{
	double res = tanh(3*y/T)-y;
	return res;
}
double func2 (double y, double T) //The free energy per site
{
	double res = 0.5*3*y*y-T*log(2*cosh(3*y)/T);
	return res;
}
//*****************************************************************************
int main()
{
	FILE *fp;
	int anyi;
	if((fp=fopen(filename,"w"))==NULL)
	{
		printf("cannot open the file: %s\n",filename);
		printf("Please input an integer to end the program:");
		scanf("%d",&anyi);
		return 0;
	}

	FILE *ffp;
	if((ffp=fopen(filename2,"w"))==NULL)
	{
		printf("cannot open the file: %s\n",filename2);
		printf("Please input an integer to end the program:");
		scanf("%d",&anyi);
		return 0;
	}

	double tem0;          //judge indicator	
	double T_step;             //the step of Temperature
	T_step = (T_high-T_low)/(N_T-1);    //note N_T is the tatal points of T
//	printf("The temperature step is %lf\n",T_step);


	double y_1;
	double y_2;

	double tem_1;
	double tem_2;

	double T = T_low;

	int i,j;    //loop indicator
	for(i=0;i<N_T;i++)
	{
		T = T_low + i*T_step;
		
		y_1=1e-1;
		y_2=1e7;
		tem_1 =  func1(y_1, T);
		tem_2 =  func1(y_2, T);
		//if(tem_1<0||tem_2>0)
		if(tem_1*tem_2>0)
		{
			printf("The two points in the boundary isn't good! Give up them now. Do it, baby!\n");
			return 0;
		}
		
		//******************************************
		
		for(j=10;j>1;j++)
		{
			tem_1 = func1(y_1, T);
			tem_2 = func1(y_2, T);
			tem0 = func1((y_1+y_2)/2.,T);
		//	printf("tem_1:%lf\ttem_2:%lf\n",tem_1,tem_2);
			if((tem_1<precision&&tem_1>=0)||(tem_1>-precision&&tem_1<=0))
			{
				fprintf(fp,"%lf\t%lf\n",T,y_1);
				fprintf(ffp,"%lf\t%lf\t%lf\n",T,func2(y_1,T),func2(-y_1,T));
				j=0;
			}
			if((tem_2<precision&&tem_2>=0)||(tem_2>-precision&&tem_2<=0))
			{
				fprintf(fp,"%lf\t%lf\n",T,y_2);
				fprintf(ffp,"%lf\t%lf\t%lf\n",T,func2(y_2,T),func2(-y_2,T));
				j=0;
			}
			if(tem_1*tem0>0)
			{
				y_1 = (y_1+y_2)/2;
			}
			if(tem_2*tem0>0)
			{
				y_2 = (y_1+y_2)/2;
			}
			printf("%lf\n",(y_1+y_2)/2); //the mediate point value

		}
	}
	return 1;
}
