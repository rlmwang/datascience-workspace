const {

    List,
    ListItem,

} = MaterialUI


const  render_output = metadata =>
    metadata.map( meta => 
        <ListItem key={ meta.name }>
            { meta.name }: { meta.value }
        </ListItem>
    )
