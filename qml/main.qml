import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

ApplicationWindow {
    id: root
    visible: true
    width: 400
    height: 750
    title: "CubAutosFinder"
    color: "#0d0d0d"

    property color gold: "#d4af37"
    property color orange: "#e85d04"
    property color card: "#1a1a1a"
    property color elevated: "#202020"
    property color text1: "#f5f5f5"
    property color text2: "#888888"

    property bool loading: apiClient.loading
    property int selectedIdx: -1

    property string filterBrand: ""
    property string filterProvince: ""
    property string filterMinPrice: ""
    property string filterMaxPrice: ""
    property var availableSources: []
    property var sourceStates: ({})
    property bool filtersVisible: false
    property int filterPanelHeight: 240

    function loadSources() {
        var xhr = new XMLHttpRequest()
        xhr.open("GET", apiClient.apiUrl + "/api/sources")
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        var resp = JSON.parse(xhr.responseText)
                        if (resp.sources && resp.sources.length > 0) {
                            availableSources = resp.sources
                            var st = ({})
                            for (var i = 0; i < resp.sources.length; i++) {
                                st[resp.sources[i].id] = true
                            }
                            sourceStates = st
                            filterPanelHeight = 200 + Math.ceil(resp.sources.length / 5) * 30
                            return
                        }
                    } catch (e) {}
                }
                useDefaultSources()
            }
        }
        xhr.send()
    }

    function useDefaultSources() {
        availableSources = [
            {id: "revolico", label: "Revolico"},
            {id: "atrexport", label: "ATR Export"},
            {id: "chinautoscuba", label: "ChinautosCuba"},
            {id: "cubamotor", label: "CubaMotor"},
            {id: "dofimall", label: "Dofimall"},
            {id: "bdc_one", label: "BDC One"},
            {id: "facebook", label: "Facebook"},
            {id: "finauto", label: "Finauto"},
            {id: "jaccuba", label: "JACCuba"},
        ]
        var st = ({})
        for (var i = 0; i < availableSources.length; i++)
            st[availableSources[i].id] = true
        sourceStates = st
        filterPanelHeight = 200 + Math.ceil(availableSources.length / 5) * 30
    }

    function buildSources() {
        var parts = []
        for (var i = 0; i < availableSources.length; i++) {
            var sid = availableSources[i].id
            if (sourceStates[sid]) parts.push(sid)
        }
        return parts.length === availableSources.length ? "" : parts.join(",")
    }

    function applyFilters() {
        filtersVisible = false
        var src = buildSources()
        var minP = parseFloat(filterMinPrice) || 0
        var maxP = parseFloat(filterMaxPrice) || 0
        apiClient.search(src, 50, minP, maxP, filterBrand, filterProvince)
    }

    function clearFilters() {
        filterBrand = ""
        filterProvince = ""
        filterMinPrice = ""
        filterMaxPrice = ""
        var st = ({})
        for (var i = 0; i < availableSources.length; i++)
            st[availableSources[i].id] = true
        sourceStates = st
    }

    function sourceChecked(sid) {
        return sourceStates[sid] !== false
    }

    function toggleSource(sid) {
        var st = sourceStates
        st[sid] = !st[sid]
        sourceStates = st
    }

    Component.onCompleted: {
        apiClient.search("", 30, 0, 0, "", "")
        loadSources()
    }

    StackView {
        id: nav
        anchors.fill: parent
        initialItem: homePage
    }

    // HOME PAGE
    Component {
        id: homePage

        Rectangle {
            color: "#0d0d0d"

            Column {
                anchors.fill: parent

                // Header
                Rectangle {
                    width: root.width
                    height: 60
                    color: "#1a1a1a"

                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 16
                        anchors.rightMargin: 16

                        Column {
                            spacing: 2
                            anchors.verticalCenter: parent.verticalCenter

                            Text { text: "CubAutos"; font.pixelSize: 18; font.bold: true; color: gold }
                            Text { text: "Vehículos Eléctricos"; font.pixelSize: 10; color: text2 }
                        }

                        Item { Layout.fillWidth: true; width: 1; height: 1; anchors.verticalCenter: parent.verticalCenter }

                        Rectangle {
                            width: 32
                            height: 32
                            radius: 16
                            border.color: gold
                            border.width: 2
                            visible: loading
                            anchors.verticalCenter: parent.verticalCenter

                            RotationAnimation on rotation {
                                from: 0; to: 360; duration: 1000; loops: Animation.Infinite
                            }
                        }

                        Text {
                            text: "✓"
                            font.pixelSize: 18
                            color: gold
                            visible: !loading
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        Item { width: 8; height: 1; anchors.verticalCenter: parent.verticalCenter }

                        // Filter button (far right)
                        Rectangle {
                            width: 32
                            height: 32
                            radius: 6
                            color: filtersVisible ? gold : "transparent"
                            border.color: gold
                            border.width: 1
                            anchors.verticalCenter: parent.verticalCenter

                            Text {
                                text: "⚙"
                                font.pixelSize: 16
                                color: filtersVisible ? "#0d0d0d" : gold
                                anchors.centerIn: parent
                            }

                            MouseArea {
                                anchors.fill: parent
                                onClicked: filtersVisible = !filtersVisible
                            }
                        }
                    }
                }

                // Status
                Rectangle {
                    width: root.width
                    height: 30
                    color: "#161616"

                    Row {
                        anchors.fill: parent
                        anchors.leftMargin: 16
                        anchors.rightMargin: 16

                        Text { text: apiClient.status; font.pixelSize: 11; color: loading ? gold : text2; anchors.verticalCenter: parent.verticalCenter }
                        Item { width: root.width - 200 }
                        Text { text: vehicleModel.count() + " resultados"; font.pixelSize: 11; color: gold; visible: vehicleModel.count() > 0; anchors.verticalCenter: parent.verticalCenter }
                    }
                }

                // Filter Panel
                Rectangle {
                    width: root.width
                    height: filtersVisible ? filterPanelHeight : 0
                    color: elevated
                    clip: true

                    Behavior on height { NumberAnimation { duration: 200; easing.type: Easing.InOutQuad } }

                    Column {
                        width: parent.width - 24
                        anchors.horizontalCenter: parent.horizontalCenter
                        y: 8
                        spacing: 8

                        // Row 1: Brand + Province
                        Row {
                            width: parent.width
                            spacing: 8

                            Rectangle {
                                width: (parent.width - 8) / 2
                                height: 32
                                color: card
                                radius: 6

                                TextInput {
                                    id: brandInput
                                    anchors.fill: parent
                                    anchors.leftMargin: 10
                                    anchors.rightMargin: 10
                                    verticalAlignment: TextInput.AlignVCenter
                                    color: text1
                                    font.pixelSize: 12
                                    text: filterBrand
                                    onTextChanged: filterBrand = text

                                    Text {
                                        text: "Marca"
                                        color: text2
                                        font.pixelSize: 12
                                        visible: parent.text === ""
                                    }
                                }
                            }

                            Rectangle {
                                width: (parent.width - 8) / 2
                                height: 32
                                color: card
                                radius: 6

                                TextInput {
                                    id: provinceInput
                                    anchors.fill: parent
                                    anchors.leftMargin: 10
                                    anchors.rightMargin: 10
                                    verticalAlignment: TextInput.AlignVCenter
                                    color: text1
                                    font.pixelSize: 12
                                    text: filterProvince
                                    onTextChanged: filterProvince = text

                                    Text {
                                        text: "Provincia"
                                        color: text2
                                        font.pixelSize: 12
                                        visible: parent.text === ""
                                    }
                                }
                            }
                        }

                        // Row 2: Min Price + Max Price
                        Row {
                            width: parent.width
                            spacing: 8

                            Rectangle {
                                width: (parent.width - 8) / 2
                                height: 32
                                color: card
                                radius: 6

                                TextInput {
                                    id: minPriceInput
                                    anchors.fill: parent
                                    anchors.leftMargin: 10
                                    anchors.rightMargin: 10
                                    verticalAlignment: TextInput.AlignVCenter
                                    color: text1
                                    font.pixelSize: 12
                                    inputMethodHints: Qt.ImhDigitsOnly
                                    text: filterMinPrice
                                    onTextChanged: filterMinPrice = text

                                    Text {
                                        text: "Precio mín. USD"
                                        color: text2
                                        font.pixelSize: 12
                                        visible: parent.text === ""
                                    }
                                }
                            }

                            Rectangle {
                                width: (parent.width - 8) / 2
                                height: 32
                                color: card
                                radius: 6

                                TextInput {
                                    id: maxPriceInput
                                    anchors.fill: parent
                                    anchors.leftMargin: 10
                                    anchors.rightMargin: 10
                                    verticalAlignment: TextInput.AlignVCenter
                                    color: text1
                                    font.pixelSize: 12
                                    inputMethodHints: Qt.ImhDigitsOnly
                                    text: filterMaxPrice
                                    onTextChanged: filterMaxPrice = text

                                    Text {
                                        text: "Precio máx. USD"
                                        color: text2
                                        font.pixelSize: 12
                                        visible: parent.text === ""
                                    }
                                }
                            }
                        }

                        // Row 3: Sources (dynamic from API)
                        Flow {
                            width: parent.width
                            spacing: 6
                            layoutDirection: Qt.LeftToRight

                            Text {
                                text: "Fuentes:"
                                color: text2
                                font.pixelSize: 11
                                height: 26
                                verticalAlignment: Text.AlignVCenter
                            }

                            Repeater {
                                model: availableSources

                                Rectangle {
                                    height: 26
                                    width: sourceLabel.width + 20
                                    radius: 4
                                    color: sourceChecked(modelData.id) ? gold : card

                                    Text {
                                        id: sourceLabel
                                        text: modelData.label || modelData.id
                                        font.pixelSize: 10
                                        font.bold: true
                                        color: sourceChecked(modelData.id) ? "#0d0d0d" : text2
                                        anchors.centerIn: parent
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: toggleSource(modelData.id)
                                    }
                                }
                            }
                        }

                        // Row 4: Apply/Clear
                        Row {
                            width: parent.width
                            spacing: 8

                            Rectangle {
                                width: (parent.width - 8) / 2
                                height: 34
                                radius: 6
                                color: gold

                                Text {
                                    text: "Aplicar Filtros"
                                    color: "#0d0d0d"
                                    font.bold: true
                                    font.pixelSize: 12
                                    anchors.centerIn: parent
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: applyFilters()
                                }
                            }

                            Rectangle {
                                width: (parent.width - 8) / 2
                                height: 34
                                radius: 6
                                color: card
                                border.color: text2
                                border.width: 1

                                Text {
                                    text: "Limpiar"
                                    color: text2
                                    font.pixelSize: 12
                                    anchors.centerIn: parent
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: clearFilters()
                                }
                            }
                        }
                    }
                }

                // Content
                Item {
                    width: root.width
                    height: root.height - 90 - (filtersVisible ? filterPanelHeight : 0)

                    Behavior on height { NumberAnimation { duration: 200; easing.type: Easing.InOutQuad } }

                    // Loading
                    Column {
                        anchors.centerIn: parent
                        visible: loading
                        spacing: 12

                        Rectangle {
                            width: 50
                            height: 50
                            radius: 25
                            border.color: gold
                            border.width: 3

                            RotationAnimation on rotation {
                                from: 0; to: 360; duration: 1200; loops: Animation.Infinite
                            }
                        }

                        Text { text: "Cargando..."; font.pixelSize: 13; color: gold; anchors.horizontalCenter: parent.horizontalCenter }
                    }

                    // List
                    ListView {
                        id: lv
                        anchors.fill: parent
                        model: vehicleModel
                        visible: !loading
                        spacing: 10
                        clip: true
                        topMargin: 8
                        bottomMargin: 8
                        leftMargin: 12
                        rightMargin: 12

                        delegate: Item {
                            width: lv.width - 24
                            height: 145

                            Rectangle {
                                anchors.fill: parent
                                color: card
                                radius: 12

                                Row {
                                    anchors.fill: parent
                                    anchors.margins: 10
                                    spacing: 10

                                    Rectangle {
                                        width: 100
                                        height: parent.height
                                        color: elevated
                                        radius: 8
                                        clip: true

                                        Image {
                                            anchors.fill: parent
                                            anchors.margins: 3
                                            fillMode: Image.PreserveAspectCrop
                                            source: imageUrl || ""
                                        }

                                        Rectangle {
                                            x: 4; y: 4
                                            width: 50; height: 16
                                            color: elevated
                                            radius: 4

                                            Text { anchors.centerIn: parent; text: sourceLabel || source || ""; color: gold; font.pixelSize: 8; font.bold: true }
                                        }
                                    }

                                    Column {
                                        width: parent.width - 120
                                        height: parent.height
                                        spacing: 6

                                        Text { text: title || ""; font.pixelSize: 12; font.bold: true; color: text1; wrapMode: Text.WordWrap; maximumLineCount: 2 }
                                        Text { text: price > 0 ? "$" + price : "Consultar"; font.pixelSize: 16; font.bold: true; color: gold }
                                        Text { text: province || "Cuba"; font.pixelSize: 11; color: text2 }
                                        Text { text: autonomiaKm > 0 ? autonomiaKm + " km" : ""; font.pixelSize: 11; color: orange; visible: autonomiaKm > 0 }
                                        Item { width: 1; height: 1 }
                                    }
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: {
                                        selectedIdx = index
                                        nav.push(detailPage)
                                    }
                                }
                            }
                        }
                    }

                    // Empty
                    Column {
                        anchors.centerIn: parent
                        visible: !loading && vehicleModel.count() === 0
                        spacing: 10

                        Text { text: "🔍"; font.pixelSize: 36; anchors.horizontalCenter: parent.horizontalCenter }
                        Text { text: "Sin resultados"; font.pixelSize: 15; font.bold: true; color: text1 }
                    }
                }
            }
        }
    }

    // DETAIL PAGE - Fixed heights
    Component {
        id: detailPage

        Rectangle {
            color: "#0d0d0d"

            Column {
                anchors.fill: parent

                // Header
                Rectangle {
                    width: root.width
                    height: 54
                    color: "#1a1a1a"

                    Text {
                        text: "← Volver"
                        font.pixelSize: 14
                        color: gold
                        anchors.left: parent.left
                        anchors.leftMargin: 16
                        anchors.verticalCenter: parent.verticalCenter

                        MouseArea { anchors.fill: parent; onClicked: nav.pop() }
                    }

                    Text {
                        text: "Detalle"
                        font.pixelSize: 16
                        font.bold: true
                        color: text1
                        anchors.centerIn: parent
                    }
                }

                // Content with fixed sections
                Column {
                    width: root.width
                    height: root.height - 54

                    // Image Gallery - 220px
                    Rectangle {
                        width: root.width
                        height: 220
                        color: card
                        clip: true

                        SwipeView {
                            id: gallerySwipe
                            anchors.fill: parent
                            interactive: true
                            clip: true
                            currentIndex: 0

                            Repeater {
                                model: vehicleModel.get(selectedIdx).images || [vehicleModel.get(selectedIdx).imageUrl || ""]

                                Item {
                                    Image {
                                        anchors.fill: parent
                                        anchors.margins: 2
                                        fillMode: Image.PreserveAspectCrop
                                        source: modelData || ""
                                    }
                                }
                            }
                        }

                        // Source badge
                        Rectangle {
                            anchors.top: parent.top
                            anchors.right: parent.right
                            anchors.margins: 10
                            width: sourceLabelBadge.width + 20
                            height: 28
                            color: gold
                            radius: 6
                            z: 2

                            Text {
                                id: sourceLabelBadge
                                anchors.centerIn: parent
                                text: vehicleModel.get(selectedIdx).sourceLabel || ""
                                color: "#0d0d0d"
                                font.pixelSize: 11
                                font.bold: true
                            }
                        }

                        // Page indicator dots
                        PageIndicator {
                            id: galleryDots
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: 4
                            anchors.horizontalCenter: parent.horizontalCenter
                            count: gallerySwipe.count
                            currentIndex: gallerySwipe.currentIndex
                            interactive: true
                            visible: count > 1
                            z: 2

                            delegate: Rectangle {
                                width: indicatorRadius * 2
                                height: indicatorRadius * 2
                                radius: indicatorRadius
                                color: index === gallerySwipe.currentIndex ? gold : "#66ffffff"

                                property int indicatorRadius: 5
                            }
                        }

                        // Nav arrows
                        Rectangle {
                            anchors.left: parent.left
                            anchors.leftMargin: 4
                            anchors.verticalCenter: parent.verticalCenter
                            width: 24; height: 24; radius: 12
                            color: "#88000000"
                            visible: gallerySwipe.count > 1 && gallerySwipe.currentIndex > 0
                            z: 2

                            Text { text: "‹"; color: "white"; font.pixelSize: 18; anchors.centerIn: parent }

                            MouseArea {
                                anchors.fill: parent
                                onClicked: gallerySwipe.currentIndex--
                            }
                        }

                        Rectangle {
                            anchors.right: parent.right
                            anchors.rightMargin: 4
                            anchors.verticalCenter: parent.verticalCenter
                            width: 24; height: 24; radius: 12
                            color: "#88000000"
                            visible: gallerySwipe.count > 1 && gallerySwipe.currentIndex < gallerySwipe.count - 1
                            z: 2

                            Text { text: "›"; color: "white"; font.pixelSize: 18; anchors.centerIn: parent }

                            MouseArea {
                                anchors.fill: parent
                                onClicked: gallerySwipe.currentIndex++
                            }
                        }
                    }

                    // Title - 85px
                    Rectangle {
                        width: root.width
                        height: 85
                        color: card

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 4

                            Text {
                                width: parent.width
                                text: vehicleModel.get(selectedIdx).title || ""
                                font.pixelSize: 15
                                font.bold: true
                                color: text1
                                wrapMode: Text.WordWrap
                                maximumLineCount: 2
                            }

                            Text {
                                text: vehicleModel.get(selectedIdx).price > 0 
                                    ? "$" + vehicleModel.get(selectedIdx).price + " " + (vehicleModel.get(selectedIdx).currency || "USD")
                                    : "Consultar precio"
                                font.pixelSize: 22
                                font.bold: true
                                color: gold
                            }

                            Text {
                                text: "📍 " + (vehicleModel.get(selectedIdx).province || "Cuba")
                                font.pixelSize: 11
                                color: text2
                            }
                        }
                    }

                    // Specs - 150px
                    Rectangle {
                        width: root.width
                        height: 150
                        color: card

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 8

                            Text {
                                text: "Especificaciones"
                                font.pixelSize: 13
                                font.bold: true
                                color: gold
                            }

                            Grid {
                                columns: 4
                                spacing: 6
                                width: parent.width

                                Rectangle {
                                    color: elevated
                                    radius: 6
                                    height: 60

                                    Column {
                                        anchors.centerIn: parent
                                        spacing: 2

                                        Text { text: "🔋"; font.pixelSize: 18; anchors.horizontalCenter: parent }
                                        Text { text: "Autonomía"; font.pixelSize: 9; color: text2; anchors.horizontalCenter: parent }
                                        Text {
                                            text: {
                                                var v = vehicleModel.get(selectedIdx).autonomiaKm
                                                return v > 0 ? v + " km" : "N/A"
                                            }
                                            font.pixelSize: 11; font.bold: true; color: text1; anchors.horizontalCenter: parent
                                        }
                                    }
                                }

                                Rectangle {
                                    color: elevated
                                    radius: 6
                                    height: 60

                                    Column {
                                        anchors.centerIn: parent
                                        spacing: 2

                                        Text { text: "⚡"; font.pixelSize: 18; anchors.horizontalCenter: parent }
                                        Text { text: "Batería"; font.pixelSize: 9; color: text2; anchors.horizontalCenter: parent }
                                        Text {
                                            text: {
                                                var v = vehicleModel.get(selectedIdx).batteryKwh
                                                return v > 0 ? v + " kWh" : "N/A"
                                            }
                                            font.pixelSize: 11; font.bold: true; color: text1; anchors.horizontalCenter: parent
                                        }
                                    }
                                }

                                Rectangle {
                                    color: elevated
                                    radius: 6
                                    height: 60

                                    Column {
                                        anchors.centerIn: parent
                                        spacing: 2

                                        Text { text: "⏱"; font.pixelSize: 18; anchors.horizontalCenter: parent }
                                        Text { text: "Carga"; font.pixelSize: 9; color: text2; anchors.horizontalCenter: parent }
                                        Text {
                                            text: vehicleModel.get(selectedIdx).chargingTime || "N/A"
                                            font.pixelSize: 11; font.bold: true; color: text1; anchors.horizontalCenter: parent
                                        }
                                    }
                                }

                                Rectangle {
                                    color: elevated
                                    radius: 6
                                    height: 60

                                    Column {
                                        anchors.centerIn: parent
                                        spacing: 2

                                        Text { text: "🚗"; font.pixelSize: 18; anchors.horizontalCenter: parent }
                                        Text { text: "Modelo"; font.pixelSize: 9; color: text2; anchors.horizontalCenter: parent }
                                        Text {
                                            text: vehicleModel.get(selectedIdx).modelo || "N/A"
                                            font.pixelSize: 11; font.bold: true; color: text1; anchors.horizontalCenter: parent
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // Contact - 90px
                    Rectangle {
                        width: root.width
                        height: 90
                        color: card

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 6

                            Text {
                                text: "Contacto"
                                font.pixelSize: 13
                                font.bold: true
                                color: gold
                            }

                            Text { text: "👤 " + (vehicleModel.get(selectedIdx).contactName || "No disponible"); font.pixelSize: 11; color: text1 }
                            Text { text: "📞 " + (vehicleModel.get(selectedIdx).contactPhone || "No disponible"); font.pixelSize: 11; color: text1 }
                            Text { text: "💬 " + (vehicleModel.get(selectedIdx).contactWhatsapp || "No disponible"); font.pixelSize: 11; color: orange }
                        }
                    }

                    // Description - 70px
                    Rectangle {
                        width: root.width
                        height: 70
                        color: card

                        Column {
                            anchors.fill: parent
                            anchors.margins: 12
                            spacing: 4

                            Text {
                                text: "Descripción"
                                font.pixelSize: 13
                                font.bold: true
                                color: gold
                            }

                            Text {
                                width: parent.width
                                text: vehicleModel.get(selectedIdx).description || "Sin descripción disponible."
                                font.pixelSize: 11
                                color: text2
                                wrapMode: Text.WordWrap
                                maximumLineCount: 3
                            }
                        }
                    }

                    // Button - 45px
                    Rectangle {
                        width: root.width
                        height: 45
                        color: gold
                        radius: 8

                        Text {
                            text: "Ver Anuncio Original"
                            color: "#0d0d0d"
                            font.bold: true
                            font.pixelSize: 14
                            anchors.centerIn: parent
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: Qt.openUrlExternally(vehicleModel.get(selectedIdx).url || "")
                        }
                    }
                }
            }
        }
    }
}