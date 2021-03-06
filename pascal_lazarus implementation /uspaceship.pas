unit uSpaceship;

{$mode objfpc}{$H+}

interface

uses
  FileUtil, Forms, Controls, Graphics, Dialogs, StdCtrls,
  Classes, SysUtils;

type
TSpaceship = class
   owner, nr, tx, ty: integer;
   x, y: real;
   function get_attack():integer;
   function on_step(player_on_turn: integer):boolean;
   constructor create(nx, ny, ntx, nty, nowner, nnr, neffective:integer);
   private
   effective: integer;
   vx, vy: real;
  end;

implementation
function TSpaceship.on_step(player_on_turn: integer):boolean;
begin
  if sqrt(sqr(tx-x)+sqr(ty-y)) <= 1 then result := true
  else begin
      {showmessage(inttostr(owner)+';'+
                  inttostr(player_on_turn)+';####'+
                  floattostr(x)+';'+
                  floattostr(y)+';');  }
      if player_on_turn = owner then begin
      x := x+vx;
      y := y+vy;
      end;
      result := false;
  end;
end;

function TSpaceship.get_attack():integer;
begin
  result := round(nr*(1-1/effective));
end;

constructor tspaceship.create(nx, ny, ntx, nty, nowner, nnr, neffective: integer);
var  abs: real;
begin
  x := real(nx);
  y := real(ny);
  tx := ntx;
  ty := nty;
  nr := nnr;
  owner := nowner;
  effective := neffective;
  abs := sqrt(sqr(tx-x)+sqr(ty-y));
  vx := real((tx-x) / abs);
  vy := real((ty-y) / abs);
end;

end.

