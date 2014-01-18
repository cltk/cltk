from cltk.corpus_compiler import Compile

#c = Compile()
c = Compile('/home/kyle/Downloads/project_dir/corps', '/home/kyle/Downloads/project_dir')
#c.dump_txts_phi5()
#c.dump_txts_phi7()
print(c.dump_txts_tlg())
