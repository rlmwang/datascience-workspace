const {
    Card,
    CardHeader,
    CardContent,
    CardActions,
    Typography,
    Button,
} = MaterialUI;


const inputWidth = '40ch'


var cards = {

useStyles: makeStyles( theme => ({
    card: {
        minWidth: 225,
        '& .MuiTextField-root': {
            width: inputWidth,
        },
    },
    form: {
    },
    button: {
        marginLeft: 'auto'
    },
}))

};



function FormCard(props) {
    const classes = cards.useStyles();
    const { children, id } = props;

return (

<form
    id = { id } 
    className={ classes.form }
    method="post" 
    encType="multipart/form-data"
>

<Card 
    className={ classes.card }
    // stub={ CardContent }
>
    <CardContent>

        { children }

    </CardContent>

    <CardActions>

        <Button
            className={ classes.button }
            color="primary"
            type="reset"
        >
            Reset
        </Button>

        <Button
            className={ classes.button }
            variant="contained"
            color="primary"
            type="submit"
        >
            Predict
        </Button>    

    </CardActions>

</Card>

</form>

)}


function BrokenCard(props) {
    
    const toArray = React.Children.toArray;
    const children = toArray(props.children);
    const Stub = props.stub;

    for (var [bkey, bchild] of children.entries()) {
        if (!React.isValidElement(bchild)) continue;
        if (bchild.type.name == "BreakPoint") break
    }

    const breakChildren = toArray(bchild.props.children);

    const [chunked, iscut] = split(breakChildren, child => (
        child.type && child.type.name === "BreakCard"
    ))

    if (chunked.length == 1) {
        children[bkey] = <Stub> { breakChildren } </Stub>
        return <Card { ...props }> { children } </Card>
    } 
    
    if (iscut[0]) {
        var head = <Card {...props}> { children.slice(0,bkey) } </Card>
    } else {
        iscut.shift()
        var head = (
            <Card {...props}> 
                { children.slice(0,bkey) } 
                <Stub> { chunked.shift() } </Stub>
            </Card>
        )
    }

    if (iscut[iscut.length-1]) {
        var foot = <Card {...props}> { children.slice(bkey+1) } </Card>
    } else {
        iscut.pop()
        var foot = (
            <Card {...props}> 
                <Stub> { chunked.pop() } </Stub>
                { children.slice(bkey+1) }
            </Card>
        )
    }

    const body = [];
    for (const [key, chunk] of chunked.entries()) {
        body[key] = iscut[key]
            ? <Fragment> { chunk } </Fragment>
            : <Card {...props} > <Stub> { chunk } </Stub> </Card>
    }

    return [head, body, foot]
}


function BrokenCardContent(props) {

    const { children } = props;

    const chunked = split(React.Children.toArray(children), child => (
        child.type && child.type.name === "BreakCard"
    ))

return (
<Fragment>
{ chunked.map((chunk, key) => 
    key % 2 == 0 ? (
        <CardContent key={ key.toString() }>
            { chunk }
        </CardContent>
    ) : (
        <Fragment key={ key.toString() }>
            { chunk }
        </Fragment>
    )
)}
</Fragment>
)}


function BreakPoint(props) {
    return props.children || undefined
}

function BreakCard(props) {
    return props.children || undefined
}


function split(array, condition) {
    // Divide array into chunks based on condition.
    // Each cut value is contained in its own chunk.
    var iscut = [];
    var chunk = [];
    var chunked = [];

    for (const val of array) {
        if (!condition(val)) {
            chunk.push(val);
            continue;
        }
        if (chunk) {
            iscut.push(false);
            chunked.push(chunk);
        }
        iscut.push(true);
        chunked.push([val]);
        chunk = [];
    }
    if (chunk) {
        iscut.push(false);
        chunked.push(chunk);
    }
    return [chunked, iscut]
}
