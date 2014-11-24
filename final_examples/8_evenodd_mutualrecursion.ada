with Ada.Text_IO, Ada.Integer_Text_IO;
use Ada.Text_IO, Ada.Integer_Text_IO;

procedure Proced2 is
   result : INTEGER;
		procedure Odd(x : in Integer; ans2 :out Integer);
		procedure Even(x : in Integer; ans1 :out Integer) is
		ans : INTEGER;
		y: INTEGER;
		begin
			if x=0 then
				ans :=1;
			else
				y:=x-1;
				Odd(y,ans);
			end if;
			ans1:=ans;
	    end Even;

		procedure Odd(x : in Integer; ans2 :out Integer) is
		ans : INTEGER;
		y: INTEGER;
		begin
			if x=0 then
				ans :=0;
			else 
				y:=x-1;
				Even(y,ans);
			end if;
			ans2:=ans;
		end Odd;
begin
   Odd(4,result);
   Print(result);
   Print_Newline(1);
   Even(4,result);
   Print(result);
   
   
   --Even(3,result);
   --Print(result);
   
end Proced2;
