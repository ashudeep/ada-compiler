with Ada.Text_IO, Ada.Integer_Text_IO;
use Ada.Text_IO, Ada.Integer_Text_IO;

procedure Proced2 is

	procedure isPrime(x: in Integer; result :out Integer) is 	
		procedure isDiv(x,y: in Integer; output: out Integer) is
			temp,z :Integer;
		begin
			temp:=x/y;
			if temp*y =x
			then
				output:=1;
			else 
				output:=0;
			end if;
			z:=1;
		end isDiv;
		flag :Integer :=0;
		temp, temp_out,z:Integer;
	begin
			for temp in 2..x-1
			loop
				isDiv(x,temp,temp_out);	
				if temp_out=1 
				then 
					flag:=1; 
				end if;
				z:=1;
			end loop;
			if flag=0 then result:=1;
			else result :=0;
			end if;
			z:=1;
	end isPrime;
	y, temp_output, z:INTEGER:=1;
	
   
begin
	for y in 2..100
	loop
		isPrime(y,temp_output);
		if temp_output=1 
		then 
			Print(y);Print_Newline(1); 
		end if;
		z:=1;
	end loop;

end Proced2;


