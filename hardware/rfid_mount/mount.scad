$fa = 1;
$fs = 0.5;
hole_r = 2.5 / 2;
cross_w = 55;
cross_l = 14;
cross_hole_w = 47.5;
rfid_w = 40;
rfid_l = 50;
th = 2.5;
l_hole = -cross_hole_w/2;
r_hole = cross_hole_w/2;

projection()
difference()
{
    mount();
    holes();
}

module mount()
{
    cube([cross_w, cross_l, th], center=true);
    cube([rfid_w, rfid_l, th], center=true);
}

module holes()
{
    translate([cross_hole_w/2,0,0])
        cylinder(r=hole_r, h=th*2, center=true);
    translate([-cross_hole_w/2,0,0])
        cylinder(r=hole_r, h=th*2, center=true);
    
    off = 10.5;
    //pi socket
    translate([l_hole + off,0,0])
        cube([2,10,th*2],center=true);
    //sel header
    translate([l_hole + off,8,0])
        cube([8,2,th*2],center=true);
    //antenna socket
    translate([l_hole + off + 27,-5.5,0])
        cube([2,5,th*2],center=true);
    //cap
    translate([l_hole + off + 24 ,-6.5,0])
        cube([6,2,th*2],center=true);
    //crystal
    translate([l_hole + off + 13 ,-7.5,0])
        cube([7,2,th*2],center=true);
    //wire hole
    translate([-rfid_w/2+5,rfid_l/2-2,0])
        cube([0.5,6,th*2],center=true);

}

