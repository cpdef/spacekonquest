#!/usr/bin/python3
class Vector(object):
    def __init__(self, rows):
        self.rows = list(rows)
        
    def x(self):
        return self.rows[0]
    
    def y(self):
        return self.rows[1]
        
    def z(self):
        return self.rows[2]
     
    def __len__(self):
        return len(self.rows)
  
    def __abs__(self):
        sqr = 0
        for value in self.rows:
            sqr += value**2
        return sqr**(0.5)
     
    def __add__(self, rows_vector):
        if len(self) != len(rows_vector):
            raise ValueError('Vector must have same len')
        return Vector([i+j for i, j in zip(self.rows, rows_vector.rows)])
        
    def __sub__(self, rows_vector):
        if len(self) != len(rows_vector):
            raise ValueError('Vector must have same len')
        return Vector([i-j for i, j in zip(self.rows, rows_vector.rows)])
        
    def __mul__(self, value):
        return Vector([i*value for i in self.rows])
        
    def norm(self, value=1):
        return Vector([i/abs(self) for i in self.rows])*value
        
    def __repr__(self):
        return '<v:{}>'.format(','.join([str(i) for i in self.rows]))
        
    def __eq__(self, vector):
        return self.rows == vector.rows
        
