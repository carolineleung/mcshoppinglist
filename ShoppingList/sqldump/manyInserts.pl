my $count;
for($count = 1  ; $count < 500; $count++) {
    print STDOUT "INSERT INTO \"shopping_list\" VALUES(" . $count . ",'item" . $count . "',0," . $count . ",'','',1297104228405,1297104228405);\n"
}

